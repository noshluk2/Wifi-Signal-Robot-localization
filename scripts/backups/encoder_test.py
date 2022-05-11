import time

import utilities as ut

time.sleep(3)


motors = ut.motor_setup(23,24,25,14,15,4)
encoders = ut.encoder_setup(22,27, 5,6)


drive_flag=True


def goal_ticks_drive( num_of_ticks):
    motors.forward()
    while(encoders.get_l_enc() < num_of_ticks ):
        motors.get_st_error(encoders.get_r_enc(),encoders.get_l_enc())
    print("Goal Reached ")
    motors.stop()

while(drive_flag):
    ## manually Spinning the wheels
    encoders.print_encoders_values()

    ## motor actuation
    # encoders.clear_encoders()
    # goal_ticks_drive( 300)
    # drive_flag=False
    # motors.motor_turn_off()





















