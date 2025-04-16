import RPi.GPIO as GPIO

dac = [8, 11, 7, 1, 0 , 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)


def dec_to_bin (num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

try:
    while True:
        val = input("Enter num from 0 to 255\n")
        try:
            i = int(val)
        except ValueError:
            try:
                floaty = float(val)
            except ValueError:
                print("Float")
            print("Not a num")

        if (i < 0):
            print('negative')
        if (i > 255):
            print('exceed the bounds')
    
        GPIO.output(dac, dec_to_bin(i))
        voltage = i * 3.3 / 256.0
        print("{:.10f}Volt".format(voltage))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()






