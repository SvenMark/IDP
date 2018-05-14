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

Stop = 0

GPIO.setup(pinPwm, GPIO.OUT)

# Set the GPIO Pin mode to be Output
GPIO.setup(pinMotorForward, GPIO.OUT)
GPIO.setup(pinMotorBackward, GPIO.OUT)

pwmMotor = GPIO.PWM(pinPwm, Frequency)

pwmMotor.start(Stop)

# Turn all motors off
def StopMotors():
	pwmMotor.ChangeDutyCycle(Stop)

# Turn both motors forwards
def Forwards(dutyCycle):
	print("Forwards " + str(dutyCycle))
	GPIO.output(pinMotorForward, GPIO.HIGH)
	GPIO.output(pinMotorBackward, GPIO.LOW)
	pwmMotor.ChangeDutyCycle(dutyCycle)

def Backwards(dutyCycle):
	print("Backwards " + str(dutyCycle))
	GPIO.output(pinMotorForward, GPIO.LOW)
	GPIO.output(pinMotorBackward, GPIO.HIGH)
	pwmMotor.ChangeDutyCycle(dutyCycle)

for cycle in range(0, 20):
	Forwards(cycle)
	time.sleep(0.5)

for cycle in range(0,20):
	Forwards(20 - cycle)
	time.sleep(0.5)

for cycle in range(0,20):
	Backwards(cycle)
	time.sleep(0.5)

for cycle in range(0,20):
	Backwards(20 - cycle)
	time.sleep(0.5)

time.sleep(2)

StopMotors()
GPIO.cleanup()


