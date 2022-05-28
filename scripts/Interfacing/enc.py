
'''
This script is to test X,Y distance traveling by manual motion to wheels
- First it is turned to manual MODE
163,164 0 Value should be replaced with 25
127,128 Should be uncommented
147,148 Should be uncommented
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
angle_fixed = True
goal_not_reached= True
l_en_a = 5
l_en_b = 6
right_motor_a = 23
right_motor_b = 24
right_motor_en = 25
des_x=0
des_y=0
left_motor_a = 14
left_motor_b = 15
left_motor_en = 4
error =0;

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

    # print("X: " , round(x,3) ," Y: " , round(y,3) , " Theta: ",round(theta,3))
    Go_to_Goal_Calculations()


def Go_to_Goal_Calculations():
    global x;global y;global theta;global des_x;global des_y;global error
    goal_x = 0.2
    goal_y = 0.3
    des_x = goal_x - x;
    des_y = goal_y - y;
    angle_to_goal = math.atan2(des_y, des_x);
    distance_to_goal  = math.sqrt(math.pow(des_x, 2) + math.pow(des_y, 2)); # distance to goal
    error = angle_to_goal - theta;




    print("Des_X: ", round(des_x,3), " Des_Y: ", round(des_y,3)," DTG :",round(distance_to_goal,3), " Error: ",round(error,3) ," ATG ", round(angle_to_goal,3) )
    Update_Motors_Speeds()
def Stop_Robot():
    pwm_1.ChangeDutyCycle(0)
    pwm_2.ChangeDutyCycle(0)

def Update_Motors_Speeds() :
    global des_x;global des_y;global error;global angle_fixed;global goal_not_reached
    rightMotorSpeed =0
    leftMotorSpeed  =  0
    # Fix error
    if(angle_fixed):
        if(error >= 0):
            rightMotorSpeed = 35
            leftMotorSpeed  =  0 ;
        else:
            angle_fixed = False
            print("\n\nAngle is set towards Goal\n\n")
        # pwm_1.ChangeDutyCycle(rightMotorSpeed)
        # pwm_2.ChangeDutyCycle(leftMotorSpeed)


    # Moving Forward
    else:
        if(goal_not_reached):
            if(des_x < 0.05 and des_y < 0.05):
                Stop_Robot();
                print("Robot Reached Goal ")
                goal_not_reached = False
            else :
                base_speed=25 # for the dutycyle being positive
                rightMotorSpeed = base_speed +  10*error ;
                leftMotorSpeed =  base_speed -  10*error  ;

                rightMotorSpeed = np.clip(rightMotorSpeed, 20, 35);
                leftMotorSpeed  = np.clip(leftMotorSpeed, 20, 35);
                print("LPWM: ",round(leftMotorSpeed,3)," RPWM ",round(rightMotorSpeed,3))

                # pwm_1.ChangeDutyCycle(45)
                # pwm_2.ChangeDutyCycle(28)
        else:
            print("Car reached the destination")



if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(right_motor_a,GPIO.OUT)
    GPIO.setup(right_motor_b,GPIO.OUT)
    GPIO.setup(right_motor_en,GPIO.OUT)
    GPIO.setup(left_motor_a,GPIO.OUT)
    GPIO.setup(left_motor_b,GPIO.OUT)
    GPIO.setup(left_motor_en,GPIO.OUT)

    pwm_1=GPIO.PWM(right_motor_en,1000)
    pwm_2=GPIO.PWM(left_motor_en,1000)
    pwm_1.start(0) # starting is turned OFF
    pwm_2.start(0)
    GPIO.output(right_motor_a,GPIO.HIGH)
    GPIO.output(right_motor_b,GPIO.LOW)
    GPIO.output(left_motor_a,GPIO.HIGH)
    GPIO.output(left_motor_b,GPIO.LOW)

    GPIO.setup(r_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(r_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(l_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(l_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(r_en_a, GPIO.BOTH, callback=Update_encR,bouncetime=20)
    GPIO.add_event_detect(l_en_a, GPIO.BOTH, callback=Update_encL,bouncetime=20)

    signal.signal(signal.SIGINT,signal_handler)
    signal.pause()


