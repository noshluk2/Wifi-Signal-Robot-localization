import RPi.GPIO as GPIO
import threading

class Encoder(object):
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
        return (self.count_L)
    
    def get_r_enc(self):
        return self.count_R
    def get_l_enc(self):
        return self.count_L
    def clear_encoders(self):
        self.count_R=0
        self.count_L=0

# r_en_a = 27 
# r_en_b = 10

# l_en_a = 5
# l_en_b = 6

# enc_obj = Encoder(27,10,5,6)

# def update_encoders():
#     threading.Timer(1,update_encoders).start()
#     print(" looping ")

# update_encoders()