"""
TinyArm IK 
Daniel Gonzalez
dgonz@mit.edu
"""
import math

def inverseKinematics(myInput):
    [x,y,z,thetaE,thetaR, gripAmount, mySpeed] = myInput
    # x = 5.125 is minimum x @ Shoulder height
    # x = 15.875 is maximum x
    # x = 11.8975 is max X @ ground and thetaE=-90
    thetaE = math.radians(thetaE)
    lg = 3.5 #inches
    l1 = 7
    l2 = 7
    xA = 1.6249
    yA = 7.125
    
    yE = z
    thetaBase = math.atan2(y,x)
    xE = math.sqrt((x**2) + (y**2))
    
    xC = xE-(lg*math.cos(thetaE))
    yC = yE-(lg * math.sin(thetaE))
    AC = math.sqrt((xC+xA)**2 + (yC-yA)**2)
    
    thetaAC = math.atan2(yC-yA,xC+xA)
    thetaA = math.acos((l2**2-l1**2-AC**2)/(-2*l1*AC))
    thetaB = math.acos((AC**2-l1**2-l2**2)/(-2*l1*l2))
    
    thetaShoulder = thetaAC + thetaA
    thetaElbow = thetaShoulder - (math.pi - thetaB)
    
    thetaBase = math.degrees(thetaBase)
    thetaShoulder = math.degrees(thetaShoulder)
    thetaElbow = math.degrees(thetaElbow)
    thetaE = math.degrees(thetaE)
    myOutput = [thetaBase, thetaShoulder, thetaElbow, thetaE, thetaR, gripAmount,mySpeed]
    return myOutput

print(str(inverseKinematics([5,5,5,10,0,0,65])))

