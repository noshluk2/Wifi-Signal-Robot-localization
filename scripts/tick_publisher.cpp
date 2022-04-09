/*
*This is a ROS node that monitors a pair of hall effect encoders and publishes
*the tick counts for a left wheel and right wheel in ROS. Whether each
*GPIO event is incremented or decremented is determined by check the direction
*signal going to the motor driver. This is written simply
*to be readable for all levels and accompanies the book Practical Robotics in C++.
*
*Author: Lloyd Brombach (lbrombach2@gmail.com)
*11/7/2019
*/

#include <pigpiod_if2.h>
#include <iostream>

using namespace std;

//GPIO Pin assignments
const int leftEncoder = 22; //left encoder
const int rightEncoder = 23; //right encoder
const int leftReverse = 13; //monitor as input that goes low when left motor set to reverse
const int rightReverse = 19; //monitor as input that goes low when right motor set to reverse

//max and min allowable values
const int encoderMin = -32768;
const int encoderMax = 32768;

int left_enc =0;
int right_enc=0;
//this is the callback function that runs when a change of state happens on the monitored gpio pin
void left_event(int pi, unsigned int gpio, unsigned int edge, unsigned int tick)
{
if(gpio_read(pi, leftReverse)==0) //decrement if motor commanded to reverse
    {
     if(left_enc==encoderMin) //handle rollunder
     {
      left_enc = encoderMax;
     }
     else
     {
      left_enc--;
     }

    }
else  //increment if not commanded to reverse (must be going forward)
    {
     if(left_enc==encoderMax) //handle rollover
     {
      left_enc = encoderMin;
     }
     else
     {
      left_enc++;
     }

    }

}
//this is the callback function that runs when a change of state happens on the monitored gpio pin
void right_event(int pi, unsigned int gpio, unsigned int edge, unsigned int tick)
{
if(gpio_read(pi, rightReverse)==0)
    {
     if(right_enc==encoderMin)
     {
      right_enc = encoderMax;
     }
     else
     {
      right_enc--;
     }
    }
else
    {
     if(right_enc==encoderMax)
      {
       right_enc = encoderMin;
      }
      else
      {
       right_enc++;
      }
    }

}

int PigpioSetup()
{
    char *addrStr = NULL;
    char *portStr = NULL;
    int pi = pigpio_start(addrStr, portStr);

    //set the mode and pullup to read the encoder like a switch
    set_mode(pi, leftEncoder, PI_INPUT);
    set_mode(pi, rightEncoder, PI_INPUT);
    set_mode(pi, leftReverse, PI_INPUT);
    set_mode(pi, rightReverse, PI_INPUT);
    set_pull_up_down(pi, leftEncoder, PI_PUD_UP);
    set_pull_up_down(pi, rightEncoder, PI_PUD_UP);
    set_pull_up_down(pi, leftReverse, PI_PUD_UP);
    set_pull_up_down(pi, rightReverse, PI_PUD_UP);

    return pi;
}

int main(int argc, char **argv)
{
    //initialize pipiod interface
    int pi = PigpioSetup();
    if(pi>=0)
    {
        cout<<"daemon interface started ok at "<<pi<<endl;
    }
    else
    {
        cout<<"Failed to connect to PIGPIO Daemon - is it running?"<<endl;
        return -1;
    }


    //initializes callbacks
    int cbLeft=callback(pi, leftEncoder,EITHER_EDGE, left_event);
    int cbRight=callback(pi, rightEncoder, EITHER_EDGE, right_event);


    while(1)
    {
        cout<<right_enc;
        cout<<left_enc;

    }

    return 0;
}
