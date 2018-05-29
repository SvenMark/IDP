from actuator import Actuator
from point import Point3D

actuator = Actuator()

rotations = actuator.inverse_kinematics(point=Point3D(90, 0, 0))

print(str(rotations))
