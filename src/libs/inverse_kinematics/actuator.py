import numpy

from libs.inverse_kinematics.core import TinyActuator
from libs.inverse_kinematics.point import Point3D


class Actuator:
    def __init__(self, cache, arm_definition, max_angles=None, min_angles=None):
        for i, val in enumerate(arm_definition):  # Fix axes
            if (arm_definition[i] == "z"):
                arm_definition[i] = "y"
            elif (arm_definition[i] == "y"):
                arm_definition[i] = "z"

        self.cache = cache

        self._arm = TinyActuator(arm_definition, max_angles=numpy.deg2rad(max_angles),
                                 min_angles=numpy.deg2rad(min_angles))

    def inverse_kinematics(self, point):
        point_string = str(point.round(2))
        if (point_string in self.cache.points):
            return self.cache.points[point_string]

        self._arm.ee = Actuator.change_format([point.x, point.y, point.z])
        angles = numpy.rad2deg(self._arm.angles)

        self.cache.points[point_string] = angles.tolist()
        self.cache.export()
        print("exported {} : {} to cache".format(point_string, angles))
        return angles

    def forward_kinematics(self, angles):
        self._arm.angles = numpy.deg2rad(angles)
        pos = Actuator.change_format(self._arm.ee)
        return Point3D(pos[0], pos[1], pos[2])

    @staticmethod
    def change_format(pos):
        return (pos[0], pos[2], pos[1])
