
import RPi.GPIO as GPIO          
import threading
import encoder_custom


class encoder_test(object):
    def __init__(self,mr_a,mr_b,mr_en,ml_a,ml_b,ml_en,mr_enc_a,mr_enc_b,ml_enc_a,ml_enc_b):
        self.mr_a=mr_a;self.mr_b=mr_b;self.ml_a=ml_a;self.ml_a=mr_a;self.ml_b=ml_b;
        self.mr_en=mr_en;self.ml_en=ml_en
        self.mr_enc_a=mr_enc_a;self.mr_enc_b=mr_enc_b;self.ml_enc_a=ml_enc_a;self.ml_enc_b=ml_enc_b;
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.mr_a, GPIO.OUT)
        GPIO.setup(self.mr_b, GPIO.OUT)
        GPIO.setup(self.mr_en,GPIO.OUT)
        GPIO.setup(self.ml_a, GPIO.OUT)
        GPIO.setup(self.ml_b, GPIO.OUT)
        GPIO.setup(self.ml_en,GPIO.OUT)
        GPIO.setup(mr_enc_a, GPIO.IN)
        GPIO.setup(ml_enc_a, GPIO.IN)
        GPIO.setup(mr_enc_b, GPIO.IN)
        GPIO.setup(ml_enc_b, GPIO.IN)
        self.enc_obj = encoder_custom.Encoder(mr_enc_a,mr_enc_b,ml_enc_a,ml_enc_b)
        self.pwm_r= GPIO.PWM(self.mr_en,1000)
        self.pwm_l = GPIO.PWM(self.ml_en,1000)        
        self.start_stop_flag=0
        self.car_turn_on()

    def car_turn_on(self):
        GPIO.output(self.mr_a,GPIO.HIGH)
        GPIO.output(self.mr_b,GPIO.LOW)
        GPIO.output(self.ml_a,GPIO.HIGH)
        GPIO.output(self.ml_b,GPIO.LOW)
        print("Car is ready to drive ")


    def drive_control(self):
        self.start_stop_flag = self.start_stop_flag + 1 
        if (self.start_stop_flag % 2 == 0 ):
            self.forward()
        else :
            self.stop()
        self.encoders_states()
        print("\n---------------\n")


    def stop(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_l.ChangeDutyCycle(0)
        print("\tStopping")

    def forward(self):
        self.pwm_r.ChangeDutyCycle(50)
        self.pwm_l.ChangeDutyCycle(50)
        print("\tForward")

    def encoders_states(self):
        print("a")
            # print(self.enc_l.pose , " / " , self.enc_r.pose)

    def start_motion(self):
        threading.Timer(1,self.drive_control).start()
    
    
   



enc_test_obj = encoder_test(23,24,25,14,15,4,27,10,5,6)
enc_test_obj.start_motion()
