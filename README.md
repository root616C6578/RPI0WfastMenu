# RPI0WfastMenu
For correct working need Raspberry Pi OS(Legacy, 32Bit)
Download ST7735 lib
```
sudo apt update
sudo apt install -y python3 python3-pip python3-pil python3-rpi.gpio

sudo apt update
sudo pip3 install gpiod gpiodevice
sudo apt install python3-spidev
sudo pip3 install RPi.GPIO
sudo pip3 install Pillow
sudo pip3 install st7735

sudo raspi-config

```
If the above method doesn't work, you can also try installing the driver manually from the source:
```
git clone https://github.com/rm-hull/st7735
cd st7735
sudo python3 setup.py install
```
https://www.waveshare.com/wiki/1.44inch_LCD_HAT
# There will be a 433MHz transmitter and reciever in the future. PS 3 option)
