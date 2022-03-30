import RPi.GPIO as GPIO          
import threading
import encoder_custom


r_en_a = 27 
r_en_b = 10

l_en_a = 5
l_en_b = 6

right_motor_a = 23
right_motor_b = 24
right_motor_en = 25

left_motor_a = 14
left_motor_b = 15
left_motor_en = 4

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
GPIO.setup(l_en_a, GPIO.IN)
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
    global enc_obj
    print(enc_obj.get_r_enc()," / " , enc_obj.get_l_enc())
    enc_obj.clear_encoders()



    
enc_obj = encoder_custom.Encoder(r_en_a,r_en_a,l_en_a,l_en_b)
Car_turn_on()
drive_control()












# import RPi.GPIO as GPIO          
# import threading
# import Encoder


# class encoder_test(object):
#     def __init__(self,mr_a,mr_b,mr_en,ml_a,ml_b,ml_en,mr_enc_a,mr_enc_b,ml_enc_a,ml_enc_b):
#         self.mr_a=mr_a;self.mr_b=mr_b;self.ml_a=mr_a;self.ml_a=mr_a;self.ml_b=ml_b;
#         self.mr_en=mr_en;self.ml_en=ml_en
#         self.mr_enc_a=mr_enc_a;self.mr_enc_b=mr_enc_b;self.ml_enc_a=ml_enc_a;self.ml_enc_b=ml_enc_b;
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.mr_a,GPIO.OUT)
#         GPIO.setup(self.mr_b,GPIO.OUT)
#         GPIO.setup(self.mr_en,GPIO.OUT)
#         GPIO.setup(self.ml_a,GPIO.OUT)
#         GPIO.setup(self.ml_b,GPIO.OUT)
#         GPIO.setup(self.ml_en,GPIO.OUT)
#         self.pwm_r= GPIO.PWM(self.mr_en,1000)
#         self.pwm_l = GPIO.PWM(self.ml_en,1000)
#         self.enc_r = Encoder.Encoder(self.mr_enc_a,self.mr_enc_b)
#         self.enc_l = Encoder.Encoder(self.ml_enc_a,self.ml_enc_b)

#         self.start_stop_flag = 0

#     def car_turn_on(self):
#         GPIO.output(self.mr_a,GPIO.HIGH)
#         GPIO.output(self.mr_b,GPIO.LOW)
#         GPIO.output(self.ml_a,GPIO.HIGH)
#         GPIO.output(self.ml_b,GPIO.LOW)


#     def drive_control(self):
#         self.start_stop_flag = self.start_stop_flag + 1 
#         if (self.start_stop_flag % 2 == 0 ):
#             self.forward()
#         else :
#             self.stop()
#         self.encoders_states()
#         print("\n---------------\n")


#     def stop(self):
#         self.pwm_r.ChangeDutyCycle(0)
#         self.pwm_l.ChangeDutyCycle(0)
#         print("\tStopping")

#     def forward(self):
#         self.pwm_r.ChangeDutyCycle(50)
#         self.pwm_l.ChangeDutyCycle(50)
#         print("\tForward")

#     def encoders_states(self):
#         print("a")
#             # print(self.enc_l.pose , " / " , self.enc_r.pose)

#     def start_motion(self):
#         threading.Timer(1,self.drive_control).start()


# enc_test_obj = encoder_test(23,24,25,14,15,4,27,10,5,6)
# enc_test_obj.car_turn_on()
# enc_test_obj.start_motion()