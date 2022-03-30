import utilities as ut
import threading

motors = ut.motor_setup(23,24,25,14,15,4)
encoders = ut.encoder_setup(27,10,5,6)

drive_flag=False
goal_ticks = 800
motors.forward()

def thread_goal_ticks():
    global drive_flag

    threading.Timer(0.5,thread_goal_ticks).start()
    remaining_ticks = goal_ticks - encoders.get_l_enc()
    if(remaining_ticks < 10):
        motors.stop()
        encoders.print_encoders_values()
        encoders.clear_encoders()
        encoders.print_encoders_values()
    else:
        print("Remaining Ticks : "remaining_ticks)


thread_goal_ticks()
