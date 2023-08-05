# Copyright 2020 Cognite AS


class Index2:
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j


class Index3(Index2):
    def __init__(self, i: int, j: int, k: int):
        super().__init__(i, j)

        self.k = k


class Position2:
    def __init__(self, i: float, j: float):
        self.i = i
        self.j = j


class Position3(Position2):
    def __init__(self, i: float, j: float, k: float):
        super().__init__(i, j)
        self.k = k
