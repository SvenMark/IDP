import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinMotorForward = 10
pinMotorBackward = 9

pinPwm = 18

# How many times to turn the pin on and off each second
Frequency = 20
# How long the pin stays on each cycle, as a percent (here, it's 30%)
DutyCycle = 30
# Setting the duty cycle to 0 means the motors will not turn
Stop = 0

# Set the GPIO Pin mode to be Output
GPIO.setup(pinMotorForward, GPIO.OUT)
GPIO.setup(pinMotorBackward, GPIO.OUT)

# Set the motor to go forward
GPIO.output(pinMotorForward, GPIO.HIGH)
GPIO.output(pinMotorBackward, GPIO.LOW)

pwmMotor = GPIO.PWM(pinPwm, Frequency)

pwmMotor.start(Stop)

# Turn all motors off
def StopMotors():
	pwmMotor.ChangeDutyCycle(Stop)

# Turn both motors forwards
def Forwards():
        GPIO.output(pinMotorForward, GPIO.HIGH)
        GPIO.output(pinMotorBackward, GPIO.LOW)
        pwmMotor.ChangeDutyCycle(DutyCycle)

def Backwards():
        GPIO.output(pinMotorForward, GPIO.LOW)
        GPIO.output(pinMotorBackward, GPIO.HIGH)
        pwmMotor.ChangeDutyCycle(DutyCycle)

Forwards()
time.sleep(1)

Backwards()
time.sleep(0.5)

StopMotors()
GPIO.cleanup()


