# Wifi-Signal-Robot-localization
This repository is for the robot which captures multiple signals from Access points in a defined area 

### Installations
#### make your Raspberry pi Wireless Control
- install vnc server and xfce
```
sudo apt install xfce4 xfce4-goodies

sudo apt get install tightvncserver

```
#### Running a screen share for RDC (remote desktop control)
- In sudo raspi-config
  - Set display reslution
  - set ssh and vnc enabled
- ssh pi@piIP # from your laptop
- vncserver :1 # in rpi ssh
- From laptop use real vnc to see screen
