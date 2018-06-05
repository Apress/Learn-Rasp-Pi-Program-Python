import os
from gps import *
from time import *
import time
import threading
import logging
from picamera import PiCamera

#set up logfile
logging.basicConfig(filename='locations.log', level=logging.DEBUG,
format='%(message)s')

camera = PiCamera()

picnum = 0
gpsd = None

class GpsPoller(threading.Thread):
    def __init__(self):      #initializes thread
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):           #actions taken by thread 
        global gpsd
        while gpsp.running:
            gpsd.next()

if  __name__ == '__main__':   #if in the main program section,
    gpsp = GpsPoller()       #start a thread and start logging
    try:                     #and taking pictures
        gpsp.start()
        while True:
            #log location from GPS
            logging.info(str(gpsd.fix.longitude) + " " + str(gpsd.fix.latitude) + " " + 
str(gpsd.fix.altitude))
        
            #save numbered image in correct directory
            camera.capture("/home/pi/Documents/plane/image" + str(picnum) + ".jpg")
            picnum = picnum + 1  #increment picture number
            time.sleep(3)
    except (KeyboardInterrupt, SystemExit):
        gpsp.running = False
        gpsp.join()
