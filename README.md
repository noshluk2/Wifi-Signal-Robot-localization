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
    pip install nmcli
    sudo apt install network-manager
    ```
    ```
    sudo chown ubuntu /dev/gpiomem
    sudo chmod g+rw /dev/gpiomem ## to access gpios
    ```

## Using This repository
- Perform noobs installation and connect rpi4 with wifi
### Running a screen share for RDC (remote desktop control)
  - Open terminal on your laptop

  ```
  ssh ubuntu@pi_IP  # IP of raspberry pi
  ## passwork is 'ubuntu'
  ```



 ### Rpi repository run
  - Obtain the repository on Raspberry pi 4

    ```
    git clone https://github.com/noshluk2/Wifi-Signal-Robot-localization
    ```
  - Run the following python file




