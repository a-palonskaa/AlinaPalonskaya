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
    val = 128
    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 64
    else:
        val += 64

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 32
    else: 
        val += 32
    

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 16
    else: 
        val += 16


    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 8
    else: 
        val += 8


    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 4
    else: 
        val += 4

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 2
    else:
        val += 2

    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 1
    else: 
        val += 1


    GPIO.output(dac, [int(bit) for bit in bin(val)[2:].zfill(8)])
    time.sleep(0.005)
    if GPIO.input(comp):
        val -= 1
    
    return val

# 0.0825286636352539

try:
    while True:
        time1 = time.time()
        code = adc()
        time2 = time.time()
        print(code*3.3/255, "   ", time2-time1)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
