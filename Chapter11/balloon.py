import os
from gps import *
import time
import threading
import subprocess

#set up variables
picnum = 0
gpsd = None

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        global picnum
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True
    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()

if __name__ == '__main__':
    gpsp = GpsPoller()
    try:
        gpsp.start()
        while True:
            f = open('position.txt', 'w')
            curAlt = gpsd.fix.altitude
            curLong = gpsd.fix.longitude
            curLat = gpsd.fix.latitude
            f.write( str(curAlt) + " feet altitude, " + str(curLong) + " degrees longitude, " + str(curLat) +
 " degrees latitude")
            f.close()
            subprocess.call(["text2wave position.txt -o position.wav"], shell = True)
            subprocess.call(['ffmpeg -i "position.wav" -y -ar 22050 "position.wav"'], shell = True)
            subprocess.call(["sudo ./pifm position.wav 103.5 22050"], shell = True)
            subprocess.call(["raspistill -o /home/pi/Documents/balloon/image" + str(picnum) + ".jpg"], shell=True)
            picnum = picnum + 1
            time.sleep(15)
    except (KeyboardInterrupt, SystemExit):
        gpsp.running = False
        gpsp.join()
