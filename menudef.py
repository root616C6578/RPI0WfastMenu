from PIL import Image, ImageDraw, ImageFont
from st7735 import ST7735
import RPi.GPIO as GPIO
import time
import subprocess

# BUTTONS
BUTTON_UP = 21
BUTTON_DOWN = 16
BUTTON_SELECT = 20
Joystick_UP = 6
Joystick_Down = 19
Joystick_Press = 13

# Setup GPIO
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Joystick_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Joystick_Down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(Joystick_Press, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Init
def setup_display():
    return ST7735(
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

# Clear Screen
def clear_screen(draw, img, disp):
    draw.rectangle((0, 0, 160, 128), outline="black", fill="black")
    disp.display(img)

# Display Menu
def display_menu(draw, disp, options, cursor, x=50, y=20):
    clear_screen(draw, img, disp)
    for i, op in enumerate(options):
        if i == cursor:
            draw.text((x, y), f"> {op}", font=font, fill="white")
        else:
            draw.text((x, y), f"  {op}", font=font, fill="white")
        y += 20
    disp.display(img)

# Get button states
def get_button_states():
    return GPIO.input(BUTTON_UP), GPIO.input(BUTTON_DOWN), GPIO.input(BUTTON_SELECT)

# Handle button navigation
def handle_button_navigation(cursor, options_length, button_up, button_down):
    if button_up == GPIO.LOW:
        cursor = (cursor - 1) % options_length
        time.sleep(0.1)
    if button_down == GPIO.LOW:
        cursor = (cursor + 1) % options_length
        time.sleep(0.1)
    return cursor

# FM Menu
def fm_menu(draw, disp, img, font):
    fm_options = ["select freq", "select wav", "start attack"]
    cursor = 0
    frequency = 87.5
    selected_file = ""
    
    # Display FM Menu
    while True:
        display_menu(draw, disp, fm_options, cursor, x=65)
        button_up, button_down, button_select = get_button_states()
        cursor = handle_button_navigation(cursor, len(fm_options), button_up, button_down)

        if button_select == GPIO.LOW:
            if fm_options[cursor] == "select freq":
                frequency = select_frequency(draw, disp, img, font, frequency)
            elif fm_options[cursor] == "select wav":
                selected_file = select_wav_file(draw, disp, img, font)
            elif fm_options[cursor] == "start attack":
                start_attack(draw, disp, img, font, frequency, selected_file)
                break

# Select frequency
def select_frequency(draw, disp, img, font, current_freq):
    while True:
        clear_screen(draw, img, disp)
        draw.text((20, 20), f"frequency: {current_freq:.1f} MHz", font=font, fill="white")
        disp.display(img)
        
        j_up = GPIO.input(Joystick_UP)
        j_down = GPIO.input(Joystick_Down)
        j_select = GPIO.input(Joystick_Press)

        if j_up == GPIO.LOW and current_freq < 107.9:
            current_freq += 0.1
            time.sleep(0.1)
        if j_down == GPIO.LOW and current_freq > 87.5:
            current_freq -= 0.1
            time.sleep(0.1)
        if j_select == GPIO.LOW:
            time.sleep(0.1)
            return round(current_freq, 1)

# Select WAV file
def select_wav_file(draw, disp, img, font):
    directory = "/home/alex/wavfiles"
    files = subprocess.run(["ls", directory], capture_output=True, text=True).stdout.splitlines()
    cursor = 0

    while True:
        clear_screen(draw, img, disp)
        y = 20
        for i, file in enumerate(files):
            if i == cursor:
                draw.text((40, y), f"> {file}", font=font, fill="white")
            else:
                draw.text((40, y), f"  {file}", font=font, fill="white")
            y += 20
        disp.display(img)

        button_up, button_down, button_select = get_button_states()
        cursor = handle_button_navigation(cursor, len(files), button_up, button_down)
        if button_select == GPIO.LOW:
            time.sleep(0.1)
            return files[cursor]

# Start attack
def start_attack(draw, disp, img, font, frequency, wav_file):
    clear_screen(draw, img, disp)
    draw.text((40, 20), f"attacking {frequency} MHz", fill="white")
    draw.text((40, 40), f"file: {wav_file}", fill="white")
    disp.display(img)

    command = ['sudo', '/home/alex/fm_transmitter/fm_transmitter', '-f', str(frequency), f"/home/alex/wavfiles/{wav_file}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end='')
    stderr = process.stderr.read()
    if stderr:
        print("Errors:", stderr)

# Main menu
def main_menu(draw, disp, img, font):
    options = ["FBCP", "HACK FM", "option 3"]
    cursor = 0

    while True:
        display_menu(draw, disp, options, cursor)
        button_up, button_down, button_select = get_button_states()
        cursor = handle_button_navigation(cursor, len(options), button_up, button_down)

        if button_select == GPIO.LOW:
            if options[cursor] == "FBCP":
                subprocess.run(["sudo", "python3", "/home/alex/mouse.py"])
                subprocess.run(["sudo", "/usr/local/bin/fbcp"])
                break
            elif options[cursor] == "HACK FM":
                fm_menu(draw, disp, img, font)

# The main def
if __name__ == "__main__":
    setup_gpio()
    disp = setup_display()
    img = Image.new("RGB", (160, 128), "black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    try:
        main_menu(draw, disp, img, font)
    finally:
        GPIO.cleanup()
