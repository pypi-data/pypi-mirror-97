# Copyright 2020 Cognite AS
import numpy as np


class Index2(np.ndarray):
    """Index 2D I and J coordinates (int)
    """

    def __new__(cls, input_array, second=None):
        if isinstance(input_array, (list, np.ndarray)):
            if len(input_array) != 2:
                raise Exception("Index can cantail only 2 values")
        else:
            input_array = np.array([input_array, second], dtype=np.int64)
        obj = np.asarray(input_array, dtype=np.int64).view(cls)
        return obj

    @property
    def i(self):
        return self[0]

    @property
    def j(self):
        return self[1]

    def __str__(self):
        return "(" + str(self.i) + ", " + str(self.j) + ")"


class Index3(Index2):
    """Index 3D I, J and K coordinates (int)
    """

    def __new__(cls, input_array, second=None, third=None):
        if isinstance(input_array, (list, np.ndarray)):
            if len(input_array) != 3:
                raise Exception("Index can cantail only 3 values")
        else:
            input_array = np.array([input_array, second, third], dtype=np.int64)
        obj = np.asarray(input_array, dtype=np.int64).view(cls)
        return obj

    @property
    def k(self):
        return self[2]

    def __str__(self):
        return "(" + str(self.i) + ", " + str(self.j) + ", " + str(self.k) + ")"


class Position2(np.ndarray):
    """Position 2D X and Y coordinates (float)
    """

    def __new__(cls, input_array, second=None):
        if isinstance(input_array, (list, np.ndarray)):
            if len(input_array) != 2:
                raise Exception("Index can cantail only 2 values")
        else:
            input_array = np.array([input_array, second], dtype=np.float64)
        obj = np.asarray(input_array, dtype=np.float64).view(cls)
        return obj

    @property
    def i(self):
        return self[0]

    @property
    def j(self):
        return self[1]

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Position3(Position2):
    """Position 3D X, Y, Z coordinates (float)
    """

    def __new__(cls, input_array, second=None, third=None):
        if isinstance(input_array, (list, np.ndarray)):
            if len(input_array) != 3:
                raise Exception("Index can cantail only 3 values")
        else:
            input_array = np.array([input_array, second, third], dtype=np.float64)
        obj = np.asarray(input_array, dtype=np.float64).view(cls)
        return obj

    @property
    def k(self):
        return self[2]

    @property
    def z(self):
        return self[2]

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
