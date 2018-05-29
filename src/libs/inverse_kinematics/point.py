from libs.inverse_kinematics import utils

class Point3D(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def negate_x(self):
        return Point3D(
            -self.x,
            self.y,
            self.z
        )

    def negate_y(self):
        return Point3D(
            self.x,
            -self.y,
            self.z
        )

    def negate_z(self):
        return Point3D(
            self.x,
            self.y,
            -self.z
        )

    def multiply_z(self, multiplier):
        return Point3D(
            self.x,
            self.y,
            self.z * multiplier
        )

    def negate(self):
        return Point3D(
            -self.x,
            -self.y,
            -self.z
        )

    @staticmethod
    def from_string(str):
        arr = str.split(',')
        return Point3D(arr[0], arr[1], arr[2])

    def rotate_around_y(self, rotate_origin=(0, 0), angle=0):
        x, z = utils.rotate(rotate_origin, (self.x, self.z), angle)

        return Point3D(
            x,
            self.y,
            z
        )

    def rotate_around_z(self, rotate_origin=(0, 0), angle=0):
        y, x = utils.rotate(rotate_origin, (self.y, self.x), angle)

        return Point3D(
            x,
            y,
            self.z
        )

    def rotate_around_x(self, rotate_origin=(0, 0), angle=0):
        z, y = utils.rotate(rotate_origin, (self.z, self.y), angle)

        return Point3D(
            self.x,
            y,
            z
        )

    def __add__(self, other):
        return Point3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __str__(self):
        return "{0},{1},{2}".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self))

    def round(self, rounder=0):
        return Point3D(
            round(self.x, rounder),
            round(self.y, rounder),
            round(self.z, rounder)
        )

OUT_OF_REACH = Point3D(999, 0, 0)