import utilities as ut
import threading
import sys
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
    x=input("Goal drive or manual drive ?  a , b ")
    if x=='a':
        x=input("Manual Drive f ,b, r, l , s ")
        

        if x=='f':
            motors.forward()
            x='z'

        elif x=='l':
            motors.left()
            x='z'

        elif x=='r':
            motors.right()
            x='z'

        elif x=='s':
            motors.stop()
            x='z'
        
    elif x=='b':
        encoders.clear_encoders()
        x=input("Number of ticks you want to move ?")
        goal_ticks_drive(int(x) )
    elif x=='e':
        motors.motor_turn_off( )
    


        

