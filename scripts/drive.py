import utilities as ut
import threading

motors = ut.motor_setup(23,24,25,14,15,4)
encoders = ut.encoder_setup(27,10, 6,5)

drive_flag=True
goal_ticks = 50

##encoders.clear_encoders()

while(1):
    x=input()
    if x=='f':
        motors.forward()
        x='z'
    elif x=='s':
        motors.stop()
        x='z'
    elif x=='e':
        encoders.clear_encoders()
        x='z'
        break
    elif x=='v':
        encoders.print_encoders_values()
        x='z'
    elif x=='l':
        print(encoders.get_l_enc())

        x='z'
    elif x=='r':
        print(encoders.get_r_enc())
        x='z'



        

