# Wifi Signal Robot Localization
This repository is for the robot which captures multiple signals from Access points in a defined area
## About
- **Scripts** directory contains all source files for testing/debuggin and developing
- **Scripts/interfacing** directory is for testing your
  - motors
  - encoders
  - gpios
- **ultilities.py** contains classes for below setups
  - Encoders
  - Motors
  - udp communication
  
## Requirments
- ### Hardware
  - Raspberry pi 4
  - 19 watt Fast Charger
  - 16gb Sdcard
  - L298D motor Driver
  - 12V DC magnetic Encoder Motors
  - 12V lipo battery
  - Srews ,pcb offsets and male to female/Male jupmer wires
- ### Software
  - Noobs on Rpi
  - Python3
  - VNC and SSH enabled
    ```
    sudo raspi-config
    ```
  - tightvnc
    ```
    sudo apt get install tightvncserver
    ```
  - xfce4

    ```
    sudo apt install xfce4 xfce4-goodies
    ```

## Using This repository
- Perform noobs installation and connect rpi4 with wifi
### Running a screen share for RDC (remote desktop control)
  - Open terminal on your laptop

  ```
  ssh pi@piIP # IP of raspberry pi
  vncserver :1 # in rpi ssh
  ```

  - From laptop use real vnc to control rpi's screen using IP:1



 ### Rpi repository run
  - Obtain the repository on Raspberry pi 4

    ```
    git clone https://github.com/noshluk2/Wifi-Signal-Robot-localization
    ```
  - Run the following python file
  
  
### Libraries Included :

- Kalman FIlter for MPU 
- - rocheparadox/kalman filter python for mpu6050

### Robot 3D models

### Electornic Connections




