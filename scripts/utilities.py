'''
This Class conatins a class to initialize encoders connected to motor as well as all motor connection for PWM driving

'''
import RPi.GPIO as GPIO
import sys
from subprocess import PIPE, Popen
from xlwt import Workbook


class encoder_setup(object):
    def __init__(self, r_en_a,r_en_b,l_en_a,l_en_b):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(r_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(r_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(l_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(l_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        self.l_en_a=l_en_a;self.l_en_b=l_en_b;
        self.r_en_a=r_en_a;self.r_en_b=r_en_b;

        GPIO.add_event_detect(r_en_a, GPIO.BOTH,
                              callback=self.Update_encR,bouncetime=5)
        GPIO.add_event_detect(l_en_a, GPIO.BOTH,
                              callback=self.Update_encL,bouncetime=5)
        self.count_R =0
        self.count_L=0

    def Update_encR(self,channel):
        if GPIO.input(self.r_en_a) == GPIO.input(self.r_en_b):
            self.count_R=self.count_R + 1
        else :
            self.count_R = self.count_R - 1
        #print(self.count_R)



    def Update_encL(self,channel):
        if GPIO.input(self.l_en_a) == GPIO.input(self.l_en_b):
            self.count_L=self.count_L + 1
        else :
            self.count_L = self.count_L - 1
        #print(self.count_L)


    def get_r_enc(self):
        return self.count_R


    def get_l_enc(self):
        return self.count_L

    def print_encoders_values(self):
        print(self.count_L, " / " ,self.count_R)


    def clear_encoders(self):
        self.count_R=0
        self.count_L=0






class motor_setup(object):
    def __init__(self,mr_a,mr_b,mr_en,ml_a,ml_b,ml_en):


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
        self.mr_a=mr_a;self.mr_b=mr_b;self.ml_a=ml_a;self.ml_a=mr_a;self.ml_b=ml_b;
        self.mr_en=mr_en;self.ml_en=ml_en
        self.pwm_r =  GPIO.PWM(mr_en,1000)
        self.pwm_l =  GPIO.PWM(ml_en,1000)
        self.pwm_l.start(0)
        self.pwm_r.start(0)
        self.left_pwm=0;



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
      self.ssid_command     = self.cmdline('iwlist wlxec086b17f505 scan |  grep "SSID"' ).decode("utf-8")
      self.mac_command = self.cmdline('iwlist wlxec086b17f505 scan |  grep "Address"' ).decode("utf-8")
      self.strength_command      = self.cmdline('iwlist wlxec086b17f505 scan |  grep "Quality"' ).decode("utf-8")
      self.file_name=file_name
      self.index =1

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

    def data_append(self):
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
        self.excel_book.save(self.file_name)

    def line_skip(self,lines=1):
        self.index=self.index + lines





