from libs.ax12 import Ax12
import RPi.GPIO as GPIO
import time


#Section dc set-up
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

#endsection dc set-up

boris = Ax12()

servo1 = 13
servo2 = 31

boris.setLedStatus(servo1, 1)
boris.setLedStatus(servo2, 1)

while True:
    Forwards(10)
    boris.move(servo1, 0)
    boris.move(servo2, 1000)
    time.sleep(0.5)

    boris.move(servo1, 1000)
    boris.move(servo2, 0)
    time.sleep(0.5)

