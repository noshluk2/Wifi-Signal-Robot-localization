'''
This script is to test the difference between Both of encoders
'''
import RPi.GPIO as GPIO
import time
import signal
import sys
from numpy import interp
import math
import numpy as np
import threading

r_en_a = 22
r_en_b = 27

l_en_a = 5
l_en_b = 6

right_motor_a = 23
right_motor_b = 24
right_motor_en = 25

left_motor_a = 14
left_motor_b = 15
left_motor_en = 4
count_R =0;count_L=0;

user_input=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(right_motor_a,GPIO.OUT)
GPIO.setup(right_motor_b,GPIO.OUT)
GPIO.setup(right_motor_en,GPIO.OUT)
GPIO.setup(left_motor_a,GPIO.OUT)
GPIO.setup(left_motor_b,GPIO.OUT)
GPIO.setup(left_motor_en,GPIO.OUT)
GPIO.setup(r_en_a, GPIO.IN)
GPIO.setup(l_en_a, GPIO.IN)
GPIO.setup(r_en_b, GPIO.IN)
GPIO.setup(l_en_b, GPIO.IN)


pwm_1=GPIO.PWM(right_motor_en,1000)
pwm_2=GPIO.PWM(left_motor_en,1000)

pwm_1.start(25)
pwm_2.start(25)


start_stop_flag =0

def Car_turn_on():
    GPIO.output(right_motor_a,GPIO.HIGH)
    GPIO.output(right_motor_b,GPIO.LOW)
    GPIO.output(left_motor_a,GPIO.HIGH)
    GPIO.output(left_motor_b,GPIO.LOW)


def drive_control():
    threading.Timer(1,drive_control).start()
    global start_stop_flag
    start_stop_flag = start_stop_flag + 1
    if (start_stop_flag % 2 == 0 ):
        forward()
    else :
        stop()
    encoders_states()
    print("\n---------------\n")


def stop():
    pwm_1.ChangeDutyCycle(0)
    pwm_2.ChangeDutyCycle(0)
    print("\tStopping")

def forward():
    pwm_1.ChangeDutyCycle(50)
    pwm_2.ChangeDutyCycle(50)
    print("\tForward")

def encoders_states():
    global count_R;global count_L
    print(count_R," / " , count_L)
    count_R=0;count_L=0;

def Update_encR(channel):
    global count_R
    if GPIO.input(r_en_a) == GPIO.input(r_en_b):
        count_R=count_R + 1
    else :
        count_R = count_R - 1
    # print("R ",count_R)
    # calculate_xy()


def Update_encL(channel):

    global count_L
    if GPIO.input(l_en_a) == GPIO.input(l_en_b):
        count_L=count_L + 1
    else :
        count_L = count_L - 1
    # print("L ",count_L)
    # calculate_xy()
GPIO.add_event_detect(r_en_a, GPIO.BOTH, callback=Update_encR,bouncetime=20)
GPIO.add_event_detect(l_en_a, GPIO.BOTH, callback=Update_encL,bouncetime=20)

Car_turn_on()
drive_control()









