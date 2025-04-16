import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

pwm = GPIO.PWM(21, 1000)
pwm.start(0)

try:
    while(True):
        val = int(input())
        pwm.ChangeDutyCycle(val)
        print("Value = {:.2f}".format(val*3.3/100))
finally:
    pwm.stop()
    GPIO.output(21, GPIO.LOW)
    GPIO.cleanup()
