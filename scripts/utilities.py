import RPi.GPIO as GPIO
from numpy import interp
import socket
class encoder_setup(object):
    def __init__(self, r_en_a,r_en_b,l_en_a,l_en_b):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(r_en_a, GPIO.IN)
        GPIO.setup(r_en_b, GPIO.IN)
        GPIO.setup(l_en_a, GPIO.IN)
        GPIO.setup(l_en_b, GPIO.IN)
        self.l_en_a=l_en_a;self.l_en_b=l_en_b;
        self.r_en_a=r_en_a;self.r_en_b=r_en_b;

        GPIO.add_event_detect(r_en_a, GPIO.BOTH, callback=self.Update_encR)
        GPIO.add_event_detect(l_en_a, GPIO.BOTH, callback=self.Update_encL)
        self.count_R =0
        self.count_L=0

    def Update_encR(self,channel):
        if GPIO.input(self.r_en_a) == GPIO.input(self.r_en_b):
            self.count_R=self.count_R + 1
        else :
            self.count_R = self.count_R - 1



    def Update_encL(self,channel):
        if GPIO.input(self.l_en_a) == GPIO.input(self.l_en_b):
            self.count_L=self.count_L + 1
        else :
            self.count_L = self.count_L - 1
        

    def get_r_enc(self):
        return self.count_R

    def get_l_enc(self):
        return self.count_L

    def print_encoders_values(self):
        print(self.count_L, " / " ,self.count_R)


    def clear_encoders(self):
        self.count_R=0
        self.count_L=0
        GPIO.cleanup()






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
        self.car_turn_on()

    def car_turn_on(self):
        
        print("Car is ready to drive ")


    def stop(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_l.ChangeDutyCycle(0)
        print("\tStopping")

    def forward(self):
        self.pwm_r.ChangeDutyCycle(30)
        self.pwm_l.ChangeDutyCycle(30)
        print("\tForward")

    def get_st_error(self,enc_r,enc_l): # Straight line error
        self.error= enc_l - enc_r
        #if positive then left encoder is moving faster
        left_pwm = 50 - self.error
        left_pwm=interp(left_pwm,[0,100],[30,50])
        self.pwm_r.ChangeDutyCycle(50)
        self.pwm_l.ChangeDutyCycle(left_pwm)
        return self.error






# class udp_message(object):
#     def __init__(self,port_number,server_ip):
#         self.port = port_number
#         self.server_ip=server_ip
#         self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#         self.sock.bind(('', self.port))
#     def data_recieved(self):
#         self.data, addr = self.sock.recvfrom(1024)
#         s=(self.data).decode()
#         return s

        # return  self.data
