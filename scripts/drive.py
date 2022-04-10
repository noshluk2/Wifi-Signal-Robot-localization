import utilities as ut
import angleOmeter_class as mpu

motors = ut.motor_setup(23,24,25,14,15,4)
encoders = ut.encoder_setup(22,27, 5,6)

drive_flag=True
goal_ticks = 50

##encoders.clear_encoders()
#motors.get_st_error(encoders.get_r_enc(),encoders.get_l_enc())

def goal_ticks_drive( num_of_ticks):
    motors.forward()
    while(encoders.get_l_enc() < num_of_ticks ):
        motors.get_st_error(encoders.get_r_enc(),encoders.get_l_enc())
    motors.stop()
    encoders.print_encoders_values()
    encoders.clear_encoders()
    print("Goal Reached ")


while(1):
    x=input("Exit or goal or mpu ? e or b or m ?")
    if x=='e':
        motors.motor_turn_off()
        x='z'
    elif x=='b':
        encoders.clear_encoders()
        goal_ticks_drive( int(x) )
        x='z'
    elif x=='m':
        mpu.get_angle()
        x='z'










