import RPi.GPIO as GPIO
import time as time

dac = [8, 11, 7, 1, 0 , 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec_to_bin (num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

try:
    period = float(input("Enter period:"))
    val = 0
    up = True

    while(True):
        GPIO.output(dac, dec_to_bin(val))

        if val == 0: up = True
        elif val == 255: up = False

        if up: val += 1  
        else: val -= 1

        time.sleep(period / 512) 

except ValueError:
    print("input err")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
