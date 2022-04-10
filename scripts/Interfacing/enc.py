import RPi.GPIO as GPIO
import time
import signal
import sys
from numpy import interp
r_en_a = 22
r_en_b = 27

l_en_a = 5
l_en_b = 6

count_R =0;count_L=0;

def signal_handler(sig,frame):
    GPIO.cleanup()
    sys.exit(0)
def Update_encR(channel):
    global count_R
    if GPIO.input(r_en_a) == GPIO.input(r_en_b):
        count_R=count_R + 1
    else :
        count_R = count_R - 1
    print("R ",count_R)



def Update_encL(channel):

    global count_L
    if GPIO.input(l_en_a) == GPIO.input(l_en_b):
        count_L=count_L + 1
    else :
        count_L = count_L - 1
    print("L ",count_L)


if __name__ == '__main__':
   GPIO.setmode(GPIO.BCM)
    GPIO.setup(r_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(r_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(l_en_a, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(l_en_b, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(r_en_a, GPIO.BOTH, callback=Update_encR,
                          bouncetime=20)
    GPIO.add_event_detect(l_en_a, GPIO.BOTH, callback=Update_encL,
                          bouncetime=20)

    signal.signal(signal.SIGINT,signal_handler)
    signal.pause()

    # print("a=-10 -> ",interp(-10,[-5,10],[50,10]) )
    # print("a=-10 -> ",interp(-10,[-5,10],[50,10]) )
    # print("a=-5 -> ",interp(-5,[-5,10],[50,10]) )
    # print("a=0 -> ",interp(0,[-5,10],[50,10]) )
    # print("a=5 -> ",interp(5,[-5,10],[50,10]) )
    # print("a=10 -> ",interp(10,[-5,10],[50,10]) )
    # print("a=10 -> ",interp(10,[-5,10],[50,10]) )

