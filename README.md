# RPI0WfastMenu
For correct working need Raspberry Pi OS(Legacy, 32Bit)
Download ST7735 lib
```
sudo apt update
sudo apt install python3-dev python3-pip python3-rpi.gpio python3-smbus libjpeg-dev libfreetype6-dev liblcms2-dev libwebp-dev libopenjp2-7-dev libharfbuzz-dev libfribidi-dev
sudo apt install python3-spidev
pip3 install Pillow
pip3 install st7735
```
If the above method doesn't work, you can also try installing the driver manually from the source:
```
git clone https://github.com/rm-hull/st7735
cd st7735
sudo python3 setup.py install
```
https://www.waveshare.com/wiki/1.44inch_LCD_HAT
# There will be a 433MHz transmitter and reciever PS 3 option)
