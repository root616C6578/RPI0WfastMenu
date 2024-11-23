from PIL import Image, ImageDraw, ImageFont
from st7735 import ST7735
import RPi.GPIO as GPIO
import time
import subprocess
# BUTTONS
BUTTON_UP = 21
BUTTON_DOWN = 16
BUTTON_SELECT = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# BUTTONS

# DISPLAY_SETTINGS
disp = ST7735(
    port=0,
    cs=0,
    dc=25,
    rst=27,
    backlight=24,
    width=128,
    height=160,
    rotation=90,
    invert=False
)
# DISPLAY_SETTINGS

# INIT
img = Image.new("RGB", (160, 128), "black")
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

listopt = ["FBCP", "HACK FM","option 3"]#, "option 4", "option 5"]
cursor = 0
x = 76  
y = 20  


while True:
    draw.rectangle((0, 0, 160, 128), outline="black", fill="black")  # РћС‡РёСЃС‚РёС‚Рё РµРєСЂР°РЅ

    
    y = 20 
    for i, op in enumerate(listopt):
        if i == cursor:
            draw.text((x, y), f"> {op}", font=font, fill="white")  # Р’РёР±СЂР°РЅРёР№ РµР»РµРјРµРЅС‚
        else:
            draw.text((x, y), f"  {op}", font=font, fill="white")  # Р†РЅС€С– РµР»РµРјРµРЅС‚Рё
        y += 20

   
    disp.display(img)
    
   
    button_state_UP = GPIO.input(BUTTON_UP)
    button_state_DOWN = GPIO.input(BUTTON_DOWN)
    button_state_SELECT = GPIO.input(BUTTON_SELECT)

    if button_state_UP == GPIO.LOW:
        cursor = (cursor - 1) % len(listopt)
        time.sleep(0.1)  
    if button_state_DOWN == GPIO.LOW:
        cursor = (cursor + 1) % len(listopt)
        time.sleep(0.1) 
    if button_state_SELECT == GPIO.LOW:  
        if listopt[cursor] == "FBCP":
            subprocess.run(["sudo", "/usr/local/bin/fbcp"])
        time.sleep(0.1) 
        if listopt[cursor] == "HACK FM":
            draw.rectangle((0, 0, 160, 128), outline="black", fill="black")
            draw.text(76, 20, "F and File")