import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 13
comp = 14

max_voltage = 2.6

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 0)

def dec2bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

def show_num_on_leds(num):
    bin_num = dec2bin(num)
    GPIO.output(leds, bin_num)


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


voltage_data = []
time_data = []

try:
    experiment_start_time = time.time()
    troyka_signal = 0
    current_voltage = 0

    #print("Begin charging capacitor")
    GPIO.output(troyka, 1)
    while(troyka_signal < 208):
        # read data from electronics
        troyka_signal = adc()
        current_voltage = troyka_signal / 256 * max_voltage

        # show real-time data to user
        #print("signal:", troyka_signal)
        #print("voltage: ",  current_voltage)
        #show_num_on_leds(troyka_signal)

        # store data in arrays
        voltage_data.append(current_voltage)
        time_data.append(time.time() - experiment_start_time)
    
    #print("Begin decharging capacitor")
    GPIO.output(troyka, 0)
    while(troyka_signal > 169):
        # read data from electronics
        troyka_signal = adc()
        current_voltage = troyka_signal / 256 * max_voltage

        # show real-time data to user
        #print("signal:", troyka_signal)
        #print("voltage: ",  current_voltage)
        #show_num_on_leds(troyka_signal)

        # store data in arrays
        voltage_data.append(current_voltage)
        time_data.append(time.time() - experiment_start_time)        

       
    experiment_finish_time = time.time()
    experiment_duration = experiment_finish_time - experiment_start_time


finally:
    GPIO.output(dac, 1)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup() 


with open("settings.txt", "w") as settings_file:
    settings_file.write(str(len(voltage_data) / experiment_duration))
    settings_file.write("\n")
    settings_file.write(str(max_voltage / 256))

voltage_data_text = "\n".join([str(i) for i in voltage_data])

with open("data.txt", "w") as ostream:
    ostream.write(voltage_data_text)


print("-------------------------------------------------------------------")
print("@a_palonskaa-------MIPT-2025---------------------------------------")
print("Experiment results:")
print("Experiment duration:", experiment_duration, "seconds")
print("Period:", experiment_duration / len(voltage_data), "seconds")
print("Frequency:", len(voltage_data) / experiment_duration, "Hz")
print("Quantization shift:", max_voltage / 256, "Volts")
print("-------------------------------------------------------------------")

plt.plot(time_data, voltage_data)
plt.show()