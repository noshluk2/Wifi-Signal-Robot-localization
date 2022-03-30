import utilities as ut
import threading

import socket
port = 5000
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', port))
motors = ut.motor_setup(23,24,25,14,15,4)
encoders = ut.encoder_setup(27,10,5,6)
data, addr = sock.recvfrom(1024) 
drive_flag=False

motors.forward()

def threaded_loop_function():
    global drive_flag
    
    threading.Timer(0.5,threaded_loop_function).start()
    # if(drive_flag):
    #     motors.forward()
    # else:
    #     motors.stop()
    # drive_flag=not drive_flag
    print(motors.get_st_error(encoders.get_l_enc() , encoders.get_r_enc()))
    encoders.clear_encoders()


threaded_loop_function()
