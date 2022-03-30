import Encoder
import threading
import time
r_en_a = 27 
r_en_b = 10

l_en_a = 5
l_en_b = 6

enc_r = Encoder.Encoder(r_en_a,r_en_b)
enc_l = Encoder.Encoder(l_en_a,l_en_b)

def update_encoders():
    threading.Timer(0.1,update_encoders).start()
    print(enc_r.pos)
    time.sleep(3)
    # b= enc_l.read()
    # print(a," / ", b)




update_encoders()

def print_encoder_values():
    print(enc_l.pose , " / " , enc_r.pose)
'''
Logic :
move for 1 sec : print encoder values

'''
 