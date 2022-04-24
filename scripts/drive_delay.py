import time
from tracemalloc import stop

import utilities as ut

time.sleep(3)


motors = ut.motor_setup(23,24,25,14,15,4)


drive_flag=True

def motion(distance):
    motors.forward()
    time.sleep(distance)
    motors.stop()

def turn_90():
    time.sleep(1)
    motors.right()
    time.sleep(0.55)
    motors.stop()
    time.sleep(1)
    print("Right turn complete")

while(drive_flag):
    print("Turning robot ON ! ")
    time.sleep(3)

    motion(2)
    turn_90()

    motion(1)
    turn_90()

    drive_flag=False
    motors.motor_turn_off()





















