'''
This Class conatins a class to initialize encoders connected to motor as well as all motor connection for PWM driving

'''
import RPi.GPIO as GPIO
import sys
from subprocess import PIPE, Popen
from xlwt import Workbook
import math
import numpy as np

class motors_enc_setup(object):
    def __init__(self,mr_a,mr_b,mr_en,ml_a,ml_b,ml_en,mr_enc,ml_enc):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(mr_a, GPIO.OUT)
        GPIO.setup(mr_b, GPIO.OUT)
        GPIO.setup(mr_en,GPIO.OUT)
        GPIO.setup(ml_a, GPIO.OUT)
        GPIO.setup(ml_b, GPIO.OUT)
        GPIO.setup(ml_en,GPIO.OUT)

        GPIO.output(mr_a,GPIO.HIGH)
        GPIO.output(mr_b,GPIO.LOW)
        GPIO.output(ml_a,GPIO.HIGH)
        GPIO.output(ml_b,GPIO.LOW)


        GPIO.setup(mr_enc, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ml_enc, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(mr_enc, GPIO.BOTH,callback=self.Update_encR,bouncetime=5)
        GPIO.add_event_detect(ml_enc, GPIO.BOTH,callback=self.Update_encL,bouncetime=5)

        self.mr_a=mr_a;self.mr_b=mr_b;self.ml_a=ml_a;self.ml_a=mr_a;self.ml_b=ml_b;
        self.mr_en=mr_en;self.ml_en=ml_en
        self.pwm_r =  GPIO.PWM(mr_en,1000)
        self.pwm_l =  GPIO.PWM(ml_en,1000)
        self.pwm_l.start(0)
        self.pwm_r.start(0)
        self.left_pwm=0;


        self.count_R =0;        self.count_L=0
        self.x = 0;self.y = 0;self.theta =0
        self.angle_fixed = True;self.goal_not_reached= True
        self.des_x=0;self.des_y=0;self.error =0;

        self.AXLE_LENGTH      = 0.129
        PULSES_PER_REVOLUTION = 135;   WHEEL_DIAMETER        = 0.067
        self.meter_per_ticks  = math.pi * WHEEL_DIAMETER / PULSES_PER_REVOLUTION

        self.go_to_goal=False ; self.goal_x=0;self.goal_y=0;


    def Update_encR(self,channel):
        self.count_R=self.count_R + 1
        if(self.go_to_goal):
            self.calculate_xy()

    def Update_encL(self,channel):
        self.count_L=self.count_L + 1
        if(self.go_to_goal):
            self.calculate_xy()

    def gtg(self,x,y):
        self.go_to_goal=True
        self.goal_x=x
        self.goal_y=y

    def calculate_xy(self):
        count_L_prev = self.count_L
        count_R_prev = self.count_R
        self.clear_encoders()

        disp_l_wheel = float(count_L_prev) * self.meter_per_ticks            # geting distance in meters each wheel has traveled
        disp_r_wheel = float(count_R_prev) * self.meter_per_ticks

        if (count_L_prev == count_R_prev):
            self.x += disp_l_wheel * math.cos(self.theta)
            self.y += disp_l_wheel * math.sin(self.theta)

        else:
            orientation_angle = (disp_r_wheel - disp_l_wheel)/self.AXLE_LENGTH
            disp_body   = (disp_r_wheel + disp_l_wheel) / 2.0;
            self.x += (disp_body/orientation_angle) * (math.sin(orientation_angle + self.theta) - math.sin(self.theta))
            self.y -= (disp_body/orientation_angle) * (math.cos(orientation_angle + self.theta) - math.cos(self.theta))
            self.theta += orientation_angle


        while(self.theta > math.pi):
            self.theta -= (2.0*math.pi)
        while(self.theta < -math.pi):
            self.theta += (2.0*math.pi)

        # print("X: " , round(self.x,3) ," Y: " , round(self.y,3) , " Theta: ",round(self.theta,3))
        self.Go_to_Goal_Calculations()

    def Go_to_Goal_Calculations(self):
        self.des_x = self.goal_x - self.x;
        self.des_y = self.goal_y - self.y;
        angle_to_goal = math.atan2(self.des_y, self.des_x);
        distance_to_goal  = math.sqrt(math.pow(self.des_x, 2) + math.pow(self.des_y, 2)); # distance to goal
        self.error = angle_to_goal - self.theta;
        print("self.des_x: ", round(self.des_x,3), " self.des_y: ", round(self.des_y,3)," DTG :",round(distance_to_goal,3), " Error: ",round(self.error,3) ," ATG ", round(angle_to_goal,3) )
        self.Update_Motors_Speeds()


    def Update_Motors_Speeds(self) :
        if(self.angle_fixed):
            if(self.error <= 0):
                self.angle_fixed = False
                print("\n\nAngle is set towards Goal\n\n")
            else:
                self.left()


        # Moving Forward
        else:
            if(self.goal_not_reached):
                if(self.des_x < 0.05 and self.des_y < 0.05):
                    self.stop();
                    print("Robot Reached Goal ")
                    self.goal_not_reached = False
                else :
                    self.forward()

            else:
                print("Car reached the destination")
                self.go_to_goal=False



    def clear_encoders(self):
        self.count_R=0
        self.count_L=0

    def stop(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_l.ChangeDutyCycle(0)

    def left(self):
        self.pwm_r.ChangeDutyCycle(30)
        self.pwm_l.ChangeDutyCycle(0)

    def right(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_l.ChangeDutyCycle(60)

    def forward(self):
        self.pwm_r.ChangeDutyCycle(30)
        self.pwm_l.ChangeDutyCycle(30)

    def get_st_error(self,enc_r,enc_l): # Straight line error
        self.error= ( enc_l - enc_r ) * 0.5
        '''
        self.left_pwm=interp(self.error,[-5,20],[35,25])
        '''
        self.pwm_r.ChangeDutyCycle(60)
        self.pwm_l.ChangeDutyCycle(58)
        #print("Error " ,self.error , "Left PWM " , self.left_pwm)
        print("Error " ,self.error , "Left PWM " , self.left_pwm)

        #return self.error
    def reached_goal(self):
        return self.go_to_goal
    def motor_turn_off(self):
        GPIO.cleanup()
        sys.exit(0)










'''
This script conatins a class to add entries of
Access points details into an excel sheet

Usage :
-> To perform 3 readings appended into excel sheet

object_=Network_data_to_excel("luqman.xls")
object_.open_sheet()


object_.data_append()
object_.line_skip()
object_.data_append()

object_.line_skip(3)
object_.data_append()

object_.save_book()


'''
class Network_data_to_excel:
    
    def __init__(self,file_name):
        self.file_name=file_name
        self.index =1
    def get_new_scan(self):
        self.ssid_command     = self.cmdline('sudo iwlist wlan0 scan |  grep "SSID"' ).decode("utf-8")
        self.mac_command      = self.cmdline('sudo iwlist wlan0 scan |  grep "Address"' ).decode("utf-8")
        self.strength_command = self.cmdline('sudo iwlist wlan0 scan |  grep "Quality"' ).decode("utf-8")

    def open_sheet(self):
        self.excel_book = Workbook()
        self.sheet = self.excel_book.add_sheet('Sheet 1')
        self.sheet.write(0, 0, 'MAC')
        self.sheet.write(0, 1, 'SSID')
        self.sheet.write(0, 2, 'SIGNAL')

    def cmdline(self,command):
        process = Popen(
            args=command,
            stdout=PIPE,
            shell=True
        )
        return process.communicate()[0]

    def spliter(self,array_in,end_space):
        array_out=[]
        for _,value in enumerate(array_in):
            array_out.append(value[end_space:])
        return array_out
    def print_data(self):
        self.get_new_scan()
        print(self.ssid_command)
        print("-"*60)
        print(self.mac_command)
        print("-"*60)
        print(self.strength_command)

    def data_append(self):
        self.get_new_scan()
        ssids= self.ssid_command.split("ESSID:")
        ssid_array=ssids[1:]

        macs= self.mac_command.split("\n")
        mac_array=self.spliter(macs,-17)

        strengths= self.strength_command.split("dBm")
        strength_array=self.spliter(strengths,-4)

        values_to_zip = zip(mac_array,ssid_array,strength_array)
        for mac,network_name,signal_strength in values_to_zip:
            self.sheet.write(self.index, 0, mac)
            self.sheet.write(self.index, 1, network_name)
            self.sheet.write(self.index, 2, signal_strength)
            self.index=self.index+1


    def save_book(self):
        print("saving book")
        self.excel_book.save(self.file_name)

    def line_skip(self,lines=1):
        self.index=self.index + lines





