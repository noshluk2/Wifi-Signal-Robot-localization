#!/usr/bin/python3
import time
import utilities as ut_obj

time.sleep(3)


motors_obj = ut_obj.motor_setup(23,24,25,14,15,4)
network_obj=ut_obj.Network_data_to_excel("venu_bot.xls")
network_obj.open_sheet()

drive_flag=True




def motion(distance):
    motors_obj.forward()
    time.sleep(distance)
    motors_obj.stop()

def turn_90():
    time.sleep(1)
    motors_obj.right()
    time.sleep(0.55)
    motors_obj.stop()
    time.sleep(1)
    print("Right turn complete")

while(drive_flag):
    print("Turning robot ON ! ")
    time.sleep(3)
    network_obj.data_append()
    network_obj.line_skip()
    network_obj.data_append()

    motion(2)
    turn_90()
    network_obj.data_append()
    network_obj.line_skip()
    network_obj.data_append()


    motion(1)
    turn_90()
    network_obj.data_append()
    network_obj.line_skip()
    network_obj.data_append()


    drive_flag=False
    motors_obj.motor_turn_off()
    network_obj.save_book()





















