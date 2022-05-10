import time
from tracemalloc import stop
import networkdata as nd
import utilities as ut

time.sleep(3)


motors = ut.motor_setup(23,24,25,14,15,4)
nd_obj=nd.Network_data_to_excel("luqman.xls")
nd_obj.open_sheet()

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
    nd_obj.data_append()
    nd_obj.line_skip()
    nd_obj.data_append()

    motion(2)
    turn_90()
    nd_obj.data_append()
    nd_obj.line_skip()
    nd_obj.data_append()


    motion(1)
    turn_90()
    nd_obj.data_append()
    nd_obj.line_skip()
    nd_obj.data_append()


    drive_flag=False
    motors.motor_turn_off()
    nd_obj.save_book()





















