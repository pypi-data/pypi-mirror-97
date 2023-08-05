# Copyright 2020 Cognite AS
import numpy as np

from .index import Position2


class AffineTransformation:
    def __init__(self, matrix=None):
        """Represents an affine transformation on the 2D Cartesian plane. It can be used to transform points. An affine transformation is a mapping of the 2D plane into itself via a series of transformations of the following basic types:
        * rotation (around the origin)
        * scaling (relative to the origin)
        * translation

        Args:
            matrix (None|array|AffineTransformation) - initial affine transformation or identity matrix
        """
        if matrix is None:
            self.matrix = np.array([1.0, 0, 0, 0, 1.0, 0], dtype=np.float64)
        elif isinstance(matrix, AffineTransformation):
            self.matrix = np.array(matrix.matrix, copy=True, dtype=np.float64)
        else:
            self.matrix = np.array(matrix, copy=True, dtype=np.float64)

    def compose(self, transformation):
        """Updates this transformation to be the composition of this transformation with the given AffineTransformation. This produces a transformation whose effect is equal to applying this transformation followed by the argument transformation. Mathematically,
        A.compose(B) = TB x TA

        Args:
            transformation (array|AffineTransformation): an affine tranformation
        Returns:
            AffineTransformation - updated affine transformation
        """
        if isinstance(transformation, AffineTransformation):
            trans = transformation.matrix
        else:
            trans = transformation
        original = self.matrix
        return AffineTransformation(
            np.array(
                [
                    original[0] * trans[0] + original[3] * trans[1],
                    original[1] * trans[0] + original[4] * trans[1],
                    original[2] * trans[0] + original[5] * trans[1] + trans[2],
                    original[0] * trans[3] + original[3] * trans[4],
                    original[1] * trans[3] + original[4] * trans[4],
                    original[2] * trans[3] + original[5] * trans[4] + trans[5],
                ]
            )
        )

    def get_scale(self, scale):
        """Get scale transformation
        |  xScale      0  dx |
        |  1      yScale  dy |
        |  0           0   1 |

        Args:
            scale (array|Position2): xScale - the value to scale by in the x direction, yScale - the value to scale by in the y direction
        Returns:
            AffineTransformation - scale transformation
        """
        p_scale = Position2(scale)
        return AffineTransformation(np.array([p_scale.i, 0.0, 0.0, 0.0, p_scale.j, 0.0], dtype=np.float64))

    def scale(self, scale):
        """Updates the value of this transformation to that of a scale transformation composed with the current value.

        Args:
            scale (array|Position2): xScale - the value to scale by in the x direction, yScale - the value to scale by in the y direction
        Returns:
            AffineTransformation - scale transformation
        """
        transfromation = self.get_scale(scale)
        return self.compose(transfromation)

    def get_translation(self, origin):
        """Gets transformation for a translation. For a translation by the vector (x, y) the transformation matrix has the value:
        |  1  0  dx |
        |  1  0  dy |
        |  0  0   1 |

        Args:
            origin (array|Position2): dx - the x component to translate by, dy - the y component to translate by
        Returns:
            AffineTransformation - translation transformation

        """
        point = Position2(origin)
        return AffineTransformation(np.array([1.0, 0, point.i, 0, 1.0, point.j], dtype=np.float64))

    def translate(self, origin):
        """Updates the value of this transformation to that of a translation transformation composed with the current value.

        Args:
            origin (array|Position2): dx - the x component to translate by, dy - the y component to translate by
        Returns:
            AffineTransformation - translation transformation
        """
        transfromation = self.get_translation(origin)
        return self.compose(transfromation)

    def get_rotation(self, theta):
        """Get this transformation to be a rotation around the origin by specifying the sin and cos of the rotation angle directly. The transformation matrix for the rotation has the value:
        |  cosTheta  -sinTheta   0 |
        |  sinTheta   cosTheta   0 |
        |         0          0   1 |

        Args:
            theta (float): rotation angle
        Returns:
            AffineTransformation - rotation transformation
        """
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        return AffineTransformation(np.array([cos_theta, -sin_theta, 0, sin_theta, cos_theta, 0], dtype=np.float64))

    def rotate(self, theta):
        """Updates the value of this transformation to that of a rotation transformation composed with the current value. Positive angles correspond to a rotation in the counter-clockwise direction.

        Args:
            theta (float): the angle to rotate by, in radians
        Returns:
            AffineTransformation - rotated transformation
        """
        transfromation = self.get_rotation(theta)
        return self.compose(transfromation)

    def inverse(self):
        """Computes the inverse of this transformation, if one exists. The inverse is the transformation which when composed with this one produces the identity transformation. A transformation has an inverse if and only if it is not singular (i.e. its determinant is non-zero). Geometrically, an transformation is non-invertible if it maps the plane to a line or a point. If no inverse exists this method will raise a Exception.

        Returns:
            AffineTransformation - inverted transformation
        """
        trans = self.matrix
        det = trans[0] * trans[4] - trans[1] * trans[3]
        if det == 0.0:
            raise Exception("Transformation is non-invertible")
        return np.array(
            [
                trans[4] / det,
                -trans[1] / det,
                (trans[1] * trans[5] - trans[2] * trans[4]) / det,
                -trans[3] / det,
                trans[0] / det,
                (-trans[0] * trans[5] + trans[3] * trans[2]) / det,
            ]
        )

    def transform(self, points):
        """Applies this transformation to the points.

        Args:
            points (2d array) - the points (N, 2)
        Returns:
            transformed points
        """
        # X: t[0] * x + t[1] * y + t[2]
        # Y: t[3] * x + t[4] * y + t[5]
        x_trans = self.matrix[0:2]
        y_trans = self.matrix[3:5]
        mult = np.array([x_trans, y_trans])
        translate = np.array([self.matrix[2], self.matrix[5]])
        return np.dot(points, mult) + translate
