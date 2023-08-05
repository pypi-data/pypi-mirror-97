# Copyright 2020 Cognite AS
import logging
import random
import time

from cognite.geospatial._client import ApiClient
from cognite.geospatial._client.exceptions import ApiException

logger = logging.getLogger("RetryClient")


class RetryApiClient(ApiClient):
    def __init__(
        self,
        configuration=None,
        token_generator=None,
        header_name=None,
        header_value=None,
        cookie=None,
        pool_threads=1,
        retry_attempts=3,
        retry_start_timeout=0.2,
        retry_max_timeout=30,
        retry_factor=2,
        retry_exceptions=None,
    ):
        super().__init__(
            configuration=configuration,
            header_name=header_name,
            header_value=header_value,
            cookie=cookie,
            pool_threads=pool_threads,
        )
        self.token_generator = token_generator
        self.retry_attempts = retry_attempts
        self.retry_max_timeout = retry_max_timeout

        self.retry_start_timeout = retry_start_timeout
        if not retry_exceptions:
            self.retry_exceptions = ApiException
        else:
            self.retry_exceptions = retry_exceptions

        self.retry_factor = retry_factor

    def request(
        self,
        method,
        url,
        query_params=None,
        headers=None,
        post_params=None,
        body=None,
        _preload_content=True,
        _request_timeout=None,
    ):
        request_call = super().request

        def handle_exception(attempt, exception):
            if isinstance(exception, ApiException):
                if (
                    exception.status == 401
                    and self.token_generator is not None
                    and self.token_generator.token_params_set()
                ):  # Unauthorized, retry if using token
                    logger.warning("Refreshing access token for this exception: %s", repr(exception))
                    self.configuration.access_token = self.token_generator.return_access_token()
                    return _do_request(attempt)
            if self.retry_exceptions and isinstance(exception, self.retry_exceptions) and attempt < self.retry_attempts:
                retry_wait = self._exponential_timeout(attempt)
                time.sleep(retry_wait)
                return _do_request(attempt)
            raise exception

        def _do_request(attempt):
            try:
                response = request_call(
                    method,
                    url,
                    query_params=query_params,
                    headers=headers,
                    post_params=post_params,
                    body=body,
                    _preload_content=_preload_content,
                    _request_timeout=_request_timeout,
                )
            except Exception as e:
                return handle_exception(attempt + 1, e)
            return response

        return _do_request(attempt=0)

    def _exponential_timeout(self, attempt) -> float:
        # https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
        timeout = self.retry_start_timeout * (self.retry_factor ** (attempt - 1))
        timeout = min(timeout, self.retry_max_timeout)
        return timeout / 2 + random.uniform(0, timeout / 2)
