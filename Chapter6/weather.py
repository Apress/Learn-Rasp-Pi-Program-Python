import os
import time
from sht1x.Sht1x import Sht1x as SHT1x
import Rpi.GPIO as GPIO
from Adafruit_BMP085 import BMP085
import smbus
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

bus = smbus.SMBus(0)
address = 0x1e

def read_byte(adr):
    return bus.read_byte_data(address,adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

def checkTemp():
    dataPin = 11
    clkPin = 7
    sht1x = SHT1x(dataPin, clkPin, SHT1x.GPIO_BOARD)
    temp = sht1x.read_temperature_C()
    temp = temp*9/5 + 32        #if you want degrees F
    return temp

def checkHumidity():
    dataPin = 11
    clkPin = 7
    sht1x = SHT1x(dataPin, clkPin, SHT1x.GPIO_BOARD)
    humidity = sht1x.read_humidity()
    return humidity

def checkBarometer():
    bmp = BMP085(0x77)
    pressure = bmp.readPressure()
    pressure = pressure/100.0
    return pressure

def checkWindSpeed()
    prev_input = 0
    total = 0
    totalSpeed = 0
    current = time.time()
    for i in range(0, 900):
        input = GPIO.input(8)
        if ((not prev_input) and input):
            total = total + 1
        prev_input = input
        if total == 90:
            rps = (1/ (time.time()-current))
            speed = math.exp((rps + 0.95)/4.3)
            totalSpeed = totalSpeed + speed
            total = 0
            current = time.time()
    speed = totalSpeed / 10    #average speed out of ten turns
    return speed

def checkWindDirection()
    write_byte(0, 0b01110000)
    write_byte(0, 0b00100000)
    write_byte(0, 0b00000000)
    scale = 0.92
    x_offset = 106        #use the offsets you computed
    yoffset = -175        #use the offsets you computed
    x_out = (read_word_2c(3) - x_offset) * scale
    y_out = (read_word_2c(7) - y_offset) * scale
    direction = math.atan2(y_out, x_out)
    if (direction < 0):
        direction += 2 * math.pi
        direction = math.degrees(direction)
    return direction

# Main program loop
while True:
    temp = checkTemp()
    humidity = checkHumidity()
    pressure = checkBarometer()
    speed = checkWindSpeed()
    direction = checkWindDirection()

    os.system("clear")
    print "Current Conditions"
    print "----------------------------------------"
    print "Temperature:        ", str(temp)
    print "Humidity:        ", str(humidity)
    print "Pressure:        ", str(pressure)
    print "Wind Speed:        ", str(speed)
    print "Wind Direction:  ", str(direction)

    time.sleep(30)
