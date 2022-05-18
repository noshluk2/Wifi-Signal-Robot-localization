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
  - Ubuntu Server 20.04
    ```
    sudo apt install python3-pip
    ```
    ```
    pip install xlwt
    ```
    ```
    pip install RPi.GPIO
    sudo apt install network-manager
    ```
    ### Give access to utilize gpios
    ```
    sudo chown ubuntu /dev/gpiomem
    sudo chmod g+rw /dev/gpiomem
    ```

## Using This repository
- Connect your RPI with Wifi -> [Video link](https://www.youtube.com/watch?v=s4ZDlV3tIuM&t=507s&ab_channel=RaspberryTips)

### Running a SSH control through terminal ( shell only )
  - Open terminal on your laptop
    - IP of raspberry pi -> get from any wifi conencted device info app
    - passwork is 'ubuntu'
  ```
  ssh ubuntu@pi_IP
  ```
 ### Rpi repository run
  - Obtain the repository on Raspberry pi 4

    ```
    git clone https://github.com/noshluk2/Wifi-Signal-Robot-localization
    ```
  - Run the following python file
    ```
    cd Wifi-Signal-Robot-localization/scripts/
    ```
    ```
    python3 drive_delay.py
    ```
  - Excel file would have been created and to check it
    ```
    ls # to see all files
    ```



