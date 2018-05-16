from entities.movement.limb.joints.dcmotor import DCMotor


class Track(object):
    """
    Base class for tracks that implements DC motors
    """

    def __init__(self, pin):
        self.motor = DCMotor(pin)

        print("Tracks setup")
        self.type = 'track'

    def forward(self, duty_cycle, delay):
        self.motor.forward(duty_cycle, delay)

    def backward(self, duty_cycle, delay):
        self.motor.backward(duty_cycle, delay)
