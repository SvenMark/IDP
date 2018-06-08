import sys
import time  # Import the Time library
import RPi.GPIO as GPIO  # Import the GPIO Library

sys.path.insert(0, '../../../../../src')


class DCMotor(object):
    """
    Base class for dc motor
    """

    def __init__(self, pin, pin_forward, pin_backward):
        """
        Constructor for the dc motor class
        :param pin: The GPIO pin the dc motor is connected to
        :param pin_forward: The forward direction pin, this pin send a signal if the motor needs to go forward
        :param pin_backward: The backward direction pin, this pin send a signal if the motor needs to go backward
        """

        # Set up the gpio and pins for the use of DC motors
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pin_motor_forward = pin_forward
        self.pin_motor_backward = pin_backward
        self.pin_pwm = pin
        self.frequency = 2048
        self.stop = 0
        self.current_speed = 0

        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_motor_forward, GPIO.OUT)
        GPIO.setup(self.pin_motor_backward, GPIO.OUT)

        # Create an instance of a pwm motor
        self.pwm_motor = GPIO.PWM(self.pin_pwm, self.frequency)
        self.pwm_motor.start(self.stop)

        print("Setup")

    def stop_motor(self):
        """
        Set the motor speed to 0
        :return: None
        """
        self.pwm_motor.ChangeDutyCycle(self.stop)
        self.current_speed = 0

    def forward(self, duty_cycle, delay):
        """
        Turn the motor forward
        :param duty_cycle: The percentage of available power the motor uses
        :param delay: Time to wait after executing
        :return: None
        """
        print("DC motor on pin " + str(self.pin_pwm) + " Forwards " + str(duty_cycle))
        GPIO.output(self.pin_motor_forward, GPIO.HIGH)
        GPIO.output(self.pin_motor_backward, GPIO.LOW)
        self.pwm_motor.ChangeDutyCycle(duty_cycle)
        self.current_speed = duty_cycle
        time.sleep(delay)

    def backward(self, duty_cycle, delay):
        """
        Turn the motor backward
        :param duty_cycle: The percentage of available power the motor uses
        :param delay: Time to wait after executing
        :return: None
        """
        print("DC motor on pin " + str(self.pin_pwm) + " Backwards " + str(duty_cycle))
        GPIO.output(self.pin_motor_forward, GPIO.LOW)
        GPIO.output(self.pin_motor_backward, GPIO.HIGH)
        self.pwm_motor.ChangeDutyCycle(duty_cycle)
        self.current_speed = duty_cycle
        time.sleep(delay)

    def clean_up(self):
        """
        Stop the motors and clean up variables and GPIO
        :return: None
        """
        self.stop_motor()
        self.current_speed = 0
        GPIO.cleanup()


def main():
    motor = DCMotor(18, 9, 10)
    motor.clean_up()


if __name__ == "__main__":
    main()
