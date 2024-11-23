import RPi.GPIO as GPIO
import time


BUTTON_UP = 21
BUTTON_DOWN = 16
BUTTON_SELECT = 20

GPIO.setmode(GPIO.BCM)  
GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
try:
    while True:
        button_state_UP = GPIO.input(BUTTON_UP)  
        if button_state_UP == GPIO.LOW: 
            print("Кнопка натиснута!1")

        button_state_SELECT = GPIO.input(BUTTON_SELECT)  
        if button_state_SELECT == GPIO.LOW: 
            print("Кнопка натиснута!2")

        button_state_DOWN = GPIO.input(BUTTON_DOWN)  
        if button_state_DOWN == GPIO.LOW: 
            print("Кнопка натиснута!3")
        time.sleep(0.1) 
except KeyboardInterrupt:
    print("Програма зупинена користувачем.")
finally:
    GPIO.cleanup() 