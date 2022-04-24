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
    
def take_turn():
    time.sleep(1)
    motors.right()
    time.sleep(0.55)
    motors.stop()
    time.sleep(1)
    encoders.clear_encoders()
    print("Right turn taken")
    
while(drive_flag):
    encoders.clear_encoders()
    
    goal_ticks_drive( 300)
    take_turn()
    goal_ticks_drive( 200 )
    take_turn()
    goal_ticks_drive( 300)
    take_turn()
    goal_ticks_drive( 200 )
    take_turn()
    goal_ticks_drive( 200 )
    take_turn()
    goal_ticks_drive( 50 )
    take_turn()
    goal_ticks_drive( 100 )
    take_turn()
    goal_ticks_drive( 50 )
    drive_flag=False
    motors.motor_turn_off()
    '''
    x=input("Exit or goal ? e or g ?")
    if x=='e':
        motors.motor_turn_off()
        x='z'
    elif x=='g':
        encoders.clear_encoders()
        x=input("Ticks or Turn ? t or r ?")
        if x=='t':
            x=input("Number of ticks")
            goal_ticks_drive( int (x) )
            encoders.print_encoders_values()
        elif x=='r':
            take_turn()    
        
        x='z'
    '''
            
            
            
            
        
            
            













