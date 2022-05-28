'''
This script is to test drive the motors and pwm signals with real time user inputs
'''
import RPi.GPIO as GPIO
from time import sleep

right_motor_a = 23
right_motor_b = 24
right_motor_en = 25

left_motor_a = 14
left_motor_b = 15
left_motor_en = 4

temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(right_motor_a,GPIO.OUT)
GPIO.setup(right_motor_b,GPIO.OUT)
GPIO.setup(right_motor_en,GPIO.OUT)
GPIO.setup(left_motor_a,GPIO.OUT)
GPIO.setup(left_motor_b,GPIO.OUT)
GPIO.setup(left_motor_en,GPIO.OUT)


GPIO.output(right_motor_a,GPIO.LOW)
GPIO.output(right_motor_b,GPIO.LOW)
GPIO.output(left_motor_a,GPIO.LOW)
GPIO.output(left_motor_b,GPIO.LOW)
pwm_1=GPIO.PWM(right_motor_en,1000)
pwm_2=GPIO.PWM(left_motor_en,1000)
pwm_1.start(25)
pwm_2.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

while(1):

    x=input()

    if x=='f':
        print("forward")
        GPIO.output(right_motor_a,GPIO.HIGH)
        GPIO.output(right_motor_b,GPIO.LOW)
        GPIO.output(left_motor_a,GPIO.HIGH)
        GPIO.output(left_motor_b,GPIO.LOW)
        temp1=1
        x='z'


    elif x=='s':
        print("stop")
        GPIO.output(right_motor_a,GPIO.LOW)
        GPIO.output(right_motor_b,GPIO.LOW)
        GPIO.output(left_motor_a,GPIO.LOW)
        GPIO.output(left_motor_b,GPIO.LOW)
        x='z'

    elif x=='r':
        print("right")
        GPIO.output(right_motor_a,GPIO.LOW)
        GPIO.output(right_motor_b,GPIO.HIGH)
        GPIO.output(left_motor_a,GPIO.HIGH)
        GPIO.output(left_motor_b,GPIO.LOW)
        temp1=0
        x='z'
    elif x=='l':
        print("left")
        GPIO.output(right_motor_b,GPIO.LOW)
        GPIO.output(right_motor_a,GPIO.HIGH)
        GPIO.output(left_motor_b,GPIO.HIGH)
        GPIO.output(left_motor_a,GPIO.LOW)
        temp1=0
        x='z'



    elif x=='b':
        print("backward")
        GPIO.output(right_motor_a,GPIO.LOW)
        GPIO.output(right_motor_b,GPIO.HIGH)
        GPIO.output(left_motor_a,GPIO.LOW)
        GPIO.output(left_motor_b,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='m':
        print("medium")
        pwm_1.ChangeDutyCycle(1)
        pwm_2.ChangeDutyCycle(1)
        x='z'

    elif x=='h':
        print("high")
        pwm_1.ChangeDutyCycle(75)
        pwm_2.ChangeDutyCycle(75)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        break

    else:
        print("<<<  wrong data  >>>")
        print("please right_motor_enter the defined data to continue.....")
