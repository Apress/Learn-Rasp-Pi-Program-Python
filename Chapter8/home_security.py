import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import string
import smtplib

GPIO.setwarnings (False)
GPIO.setmode (GPIO.BOARD)
time_stamp = time.time() #for debouncing
camera = PiCamera()

#set pins
#pin 11 = motion sensor
GPIO.setup (11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#pin 13 = magnetic sensor
GPIO.setup (13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#pin 15 = limit switch
GPIO.setup (15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#pin 19 = pressure switch
GPIO.setup (19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def take_pic(sensor):
    camera.capture(sensor + “.jpg”)
    time.sleep(0.5) #wait 1/2 second for pic to be taken before continuing

def send_text(details):
    HOST = “smtp.gmail.com”
    SUBJECT = “Break-in!”
    TO = “xxxxxxxxxx@txt.att.net”
    FROM = “python@mydomain.com”
    text = details
    BODY = string.join(("From: %s" % FROM, "To: %s" % TO, "Subject: %s" % SUBJECT, "", text), "\r\n")
    s = smtplib.SMTP(‘smtp.gmail.com’,587)
    s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.login(“username@gmail.com”, “mypassword”)
    s.sendmail(FROM, [TO], BODY)
    s.quit()

def motion_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3: #check for debouncing
        print "Motion detector detected."
        send_text(“Motion detector”)
        take_pic(“motion”)
    time_stamp = time_now

def limit_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3: #check for debouncing
        print "Limit switch pressed."
        send_text(“Limit switch”)
        take_pic(“limit”)
    time_stamp = time_now

def magnet_callback(channel):
    global time_stamp
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3: #check for debouncing
        print "Magnetic sensor tripped."
        send_text(“Magnetic sensor”)
        take_pic(“magnet”)
    time_stamp = time_now

#main body
raw_input("Press enter to start program\n")

GPIO.add_event_detect(11, GPIO.RISING, callback=motion_callback)
GPIO.add_event_detect(13, GPIO.RISING, callback=magnet_callback)
GPIO.add_event_detect(15, GPIO.RISING, callback=limit_callback)

# pressure switch ends the program
# you could easily add a unique callback for the pressure switch
# and add another switch just to turn off the network
try:
    print "Waiting for sensors..."
    GPIO.wait_for_edge(19, GPIO.RISING)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
