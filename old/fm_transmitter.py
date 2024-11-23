# import readchar
# import os

# f = 87.0


# while True:
    
#     os.system("cls")
    
#     print(f"Поточне значення: {f:.1f}")
#     key = readchar.readkey()
    
#     if key == 'q':  
#         break
#     elif key == 'w':
#         if f < 107.9: 
#             f += 0.10 
    
#     elif key == 's':
#         if f > 87.0:  
#             a -= 0.10
#     elif key == '\r':
#         fm = round(f, 1)
#         print(f"Кінцеве значення: {fm}")
#         print(f"{fm}")
#         i = [fm]
#         print(i)
#         break
# input()
from PIL import Image, ImageDraw, ImageFont
from st7735 import ST7735
import RPi.GPIO as GPIO
import time
import subprocess

# BUTTONS
BUTTON_UP = 21
BUTTON_DOWN = 16
BUTTON_SELECT = 20
Joystick_UP	= 6	
Joystick_Down = 19	
Joystick_Press = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(Joystick_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Joystick_Down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Joystick_Press, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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



listopt = ["FBCP", "HACK FM", "option 3"]  # Список опцій
fm_opt = ["select freq", "select wav", "start attack"] # Список фм опцій



cursor = 0
x = 60  
y = 20  

while True:
    draw.rectangle((0, 0, 160, 128), outline="black", fill="black")  # Очистити екран

    # Відображення меню
    y = 20 
    for i, op in enumerate(listopt):
        if i == cursor:
            draw.text((x, y), f"> {op}", font=font, fill="white")  # Вибраний елемент
        else:
            draw.text((x, y), f"  {op}", font=font, fill="white")  # Інші елементи
        y += 20

    disp.display(img)  # Оновлення екрану

    # Читання стану кнопок
    button_state_UP = GPIO.input(BUTTON_UP)
    button_state_DOWN = GPIO.input(BUTTON_DOWN)
    button_state_SELECT = GPIO.input(BUTTON_SELECT)

    # Обробка кнопок
    if button_state_UP == GPIO.LOW:
        cursor = (cursor - 1) % len(listopt)
        time.sleep(0.1)  
    if button_state_DOWN == GPIO.LOW:
        cursor = (cursor + 1) % len(listopt)
        time.sleep(0.1) 
    if button_state_SELECT == GPIO.LOW:  
        if listopt[cursor] == "FBCP":
            subprocess.run(["sudo", "/usr/local/bin/fbcp"])
            subprocess.run(["sudo", "python3", "/home/alex/mouse.py"])
            break
        time.sleep(0.1)
        if listopt[cursor] == "HACK FM":
            
            draw.rectangle((0, 0, 160, 128), outline="black", fill="black")  # Очистити екран
            disp.display(img)
            
            f = 87.5
            fm = 0.0
            directory = "/home/alex/wavfiles" 
            command = ["ls", directory]
            result = subprocess.run(command, capture_output=True, text=True)
            files = result.stdout.splitlines()
            wavfiles = files
            selected_file = ''
            while True:
                draw.rectangle((0, 0, 160, 128), outline="black", fill="black")
                y = 20 
                for i, op in enumerate(fm_opt):
                    if i == cursor:
                        draw.text((65.5, y), f"> {op}", font=font, fill="white")  # Вибраний елемент
                    else:
                        draw.text((65.5, y), f"  {op}", font=font, fill="white") 
                    y += 20
                disp.display(img)  # Оновлення екран  

                # Читання стану кнопок
                button_state_UP = GPIO.input(BUTTON_UP)
                button_state_DOWN = GPIO.input(BUTTON_DOWN)
                button_state_SELECT = GPIO.input(BUTTON_SELECT)  

                # Обробка кнопок
                if button_state_UP == GPIO.LOW:
                    cursor = (cursor - 1) % len(listopt)
                    time.sleep(0.1)  
                if button_state_DOWN == GPIO.LOW:
                    cursor = (cursor + 1) % len(listopt)
                    time.sleep(0.1) 

                #Select
                if button_state_SELECT == GPIO.LOW:
                    if fm_opt[cursor] == "select freq":
                        while True:
                            draw.rectangle((0, 0, 160, 128), outline="black", fill="black")
                            draw.text((30, 20), f"frequency: {f:.1f} MHz", font=font, fill="white")
                            disp.display(img)

                            button_state_JUP = GPIO.input(Joystick_UP)
                            button_state_JDOWN = GPIO.input(Joystick_Down)
                            button_state_JSELECT = GPIO.input(Joystick_Press)

                            if button_state_JUP == GPIO.LOW and f < 107.9:
                                f += 0.1
                                f = round(f, 1)
                                draw.text((30, 20), f"frequency: {f:.1f} MHz", font=font, fill="white")
                                time.sleep(0.1)
                    
                            if button_state_JDOWN == GPIO.LOW and f > 87.5:
                                f -= 0.1
                                f = round(f, 1)
                                draw.text((30, 20), f"frequency: {f:.1f} MHz", font=font, fill="white")
                                time.sleep(0.1)                    

                            if button_state_JSELECT == GPIO.LOW:
                                fm = round(f, 1)
                                print(fm)
                                time.sleep(0.1)
                                break
                    time.sleep(0.1)
                    if fm_opt[cursor] == "select wav":
                        cursor_wav = 0
                        while True:
                            
                            draw.rectangle((0, 0, 160, 128), outline="black", fill="black")
                            y = 20 
                            for i, op in enumerate(wavfiles):
                                if i == cursor_wav:
                                    draw.text((65.5, y), f"> {op}", font=font, fill="white")  # Вибраний елемент
                                else:
                                    draw.text((65.5, y), f"  {op}", font=font, fill="white") 
                                y += 20
                            disp.display(img)    

                            
                            button_state_UP = GPIO.input(BUTTON_UP)
                            button_state_DOWN = GPIO.input(BUTTON_DOWN)
                            button_state_SELECT = GPIO.input(BUTTON_SELECT)  

                            # Обробка кнопок
                            if button_state_UP == GPIO.LOW:
                                cursor_wav = (cursor_wav - 1) % len(listopt)
                                time.sleep(0.1)  
                            if button_state_DOWN == GPIO.LOW:
                                cursor_wav = (cursor_wav + 1) % len(listopt)
                                time.sleep(0.1)
                            if button_state_SELECT == GPIO.LOW:
                                selected_file = wavfiles[cursor_wav]
                                print(f"Selected WAV file: {selected_file}")
                                time.sleep(0.1)
                                break
                    time.sleep(0.1)

                    if fm_opt[cursor] == "start attack":
                        print(fm)
                        print(selected_file)
                        time.sleep(0.1)
                        break
        time.sleep(2)
        

