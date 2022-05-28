
'''
This script is to test X,Y distance traveling by manual motion to wheels
'''
import RPi.GPIO as GPIO
import time
import signal
import sys
from numpy import interp
import math
import numpy as np

r_en_a = 22
r_en_b = 27

l_en_a = 5
l_en_b = 6

AXLE_LENGTH           = 0.129
PULSES_PER_REVOLUTION = 135
WHEEL_DIAMETER        = 0.067
meter_per_ticks       = math.pi * WHEEL_DIAMETER / PULSES_PER_REVOLUTION;
count_R =0;count_L=0;
x = 0
y = 0
theta =0
def signal_handler(sig,frame):
    GPIO.cleanup()
    sys.exit(0)

def Update_encR(channel):
    global count_R
    if GPIO.input(r_en_a) == GPIO.input(r_en_b):
        count_R=count_R + 1
    else :
        count_R = count_R - 1
    # print("R ",count_R)
    calculate_xy()


def Update_encL(channel):

    global count_L
    if GPIO.input(l_en_a) == GPIO.input(l_en_b):
        count_L=count_L + 1
    else :
        count_L = count_L - 1
    # print("L ",count_L)
    calculate_xy()

def calculate_xy():
    global count_L;global count_R;global x;global theta;global y
    count_L_prev = count_L
    count_R_prev = count_R
    count_L      = 0
    count_R      = 0
    disp_l_wheel = float(count_L_prev) * meter_per_ticks            # geting distance in meters each wheel has traveled
    disp_r_wheel = float(count_R_prev) * meter_per_ticks

    if (count_L_prev == count_R_prev):
        x += disp_l_wheel * math.cos(theta)
        y += disp_l_wheel * math.sin(theta)

    else:
        orientation_angle = (disp_r_wheel - disp_l_wheel)/AXLE_LENGTH
        disp_body   = (disp_r_wheel + disp_l_wheel) / 2.0;
        x += (disp_body/orientation_angle) * (math.sin(orientation_angle + theta) - math.sin(theta))
        y -= (disp_body/orientation_angle) * (math.cos(orientation_angle + theta) - math.cos(theta))
        theta += orientation_angle


    while(theta > math.pi):
        theta -= (2.0*math.pi)
    while(theta < -math.pi):
        theta += (2.0*math.pi)
    print("Theta = ",theta)
    # print(round(x,3) ," / " , round(y,3) , " / ",round(theta,3))
    Go_to_Goal_Calculations()


def Go_to_Goal_Calculations():
    global x;global y;global theta
    goal_x = 6
    goal_y =0
    des_x = goal_x - x;
    des_y = goal_y - y;
    angle_to_goal = math.atan2(des_y, des_x);
    distance_to_goal  = math.sqrt(pow(des_x, 2) + pow(des_y, 2)); # distance to goal
    error = angle_to_goal - theta;
    # print("Remaining X Y = ", des_x, " / ", des_y)
    print("Error = ", error)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(r_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(r_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(l_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(l_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(r_en_a, GPIO.BOTH, callback=Update_encR,bouncetime=20)
    GPIO.add_event_detect(l_en_a, GPIO.BOTH, callback=Update_encL,bouncetime=20)

    signal.signal(signal.SIGINT,signal_handler)
    signal.pause()


