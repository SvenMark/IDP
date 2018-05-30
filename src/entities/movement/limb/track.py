import sys

sys.path.insert(0, '../../../../src')

from entities.movement.limb.joints.dcmotor import DCMotor


class Track(object):
    def __init__(self, track_pin, pin_forward, pin_backward):
        """
        Constructor for track class which is almost direct copy of dc motor
        :param track_pin: The PWM pin which sets the speed
        :param pin_forward: The forward direction pin
        :param pin_backward: The backward direction pin
        """

        # Initialise both motors as tracks. Each track has 1 motor.
        self.motor = DCMotor(track_pin, pin_forward, pin_backward)
        self.current_speed = 0
        self.type = 'track'

        print("Track setup")

    def stop_motor(self):
        """
        Set the motor speed to 0
        :return: None
        """
        self.motor.stop_motor()
        self.current_speed = 0

    def forward(self, duty_cycle, delay):
        """
        Turn the motor forward
        :param duty_cycle: The percentage of available power the motor uses
        :param delay: Time to wait after executing
        :return: None
        """
        self.motor.forward(duty_cycle, delay)

    def backward(self, duty_cycle, delay):
        """
        Turn the motor backward
        :param duty_cycle: The percentage of available power the motor uses
        :param delay: Time to wait after executing
        :return: None
        """
        self.motor.backward(duty_cycle, delay)

    def clean_up(self):
        """
        Stop the motors and clean up variables and GPIO
        :return: None
        """
        self.motor.clean_up()
        self.current_speed = 0

