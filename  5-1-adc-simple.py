import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, GPIO.PUD_OFF, GPIO.HIGH)

def DecToBin(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]

def adc():
    for i in range(256):
        GPIO.output(dac, DecToBin(i))
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            return i
    return 256

try:
    while True:
        val = adc()
        print(val*3.3/256)
        time.sleep(0.5)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()