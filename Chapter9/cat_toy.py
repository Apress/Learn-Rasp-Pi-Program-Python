import RPi.GPIO as GPIO
import time
import random
random.seed()

#set pins
GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings (False)
GPIO.setup (11, GPIO.OUT) #laser power
GPIO.setup (13, GPIO.OUT) #X-servo
GPIO.setup (15, GPIO.OUT) #Y-servo
GPIO.setup (19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #in from IR

#setup servo pwm
p = GPIO.PWM (13, 50)
q = GPIO.PWM (15, 50)

#set both servos to center to start
p.start (7.5)
q.start (7.5)

def moveServos():
    "Turns on laser and moves X- and Y-servos randomly"
    lightLaser ()

    p.ChangeDutyCycle (random.randint (8, 12))
    time.sleep (random.random())
    q.ChangeDutyCycle (random.randint (8, 12))
    time.sleep (random.random())

    p.ChangeDutyCycle (random.randint (3, 5))
    time.sleep (random.random())
    q.ChangeDutyCycle (random.randint (3, 5))
    time.sleep (random.random())

    dimLaser ()

def lightLaser():
    GPIO.output (11, 1)

def dimLaser():
    GPIO.output (11, 0)

#main loop
while True:
    #check for input from sensor
    if GPIO.input (19):
        moveServos()
        time.sleep (0.5) #wait a half sec before polling sensor
    else:
        dimLaser()
        time.sleep (0.5)
