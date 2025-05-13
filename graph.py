import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
import math

with open("./settings.txt", "r") as settings_file:
    settings_data = [float(num) for num in settings_file.read().split("\n")]

data_arr = np.loadtxt("./data.txt", dtype=int)

volt_step = settings_data[1]
time_step = settings_data[0]

volt_arr = data_arr * volt_step
time_arr = np.arange(0, len(data_arr)) * time_step

volt_max = np.max(volt_arr)
volt_max_ind = np.argmax(volt_arr)
time_max = time_arr[-1]
time_max_ind = len(time_arr) - 1

charge_data = [time_arr[:volt_max_ind + 1], volt_arr[:volt_max_ind + 1]]
discharge_data = [time_arr[volt_max_ind:], volt_arr[volt_max_ind:]]

figure, axes = plt.subplots(figsize=(16, 10), dpi=400)

axes.set_xlabel("Время, с", fontsize=16)
axes.set_ylabel("Напряжение, В", fontsize=16)
axes.set_title("Процесс заряда и разряда конденсатора\nв RC-цепочке (экспериментальные данные)", fontsize=20, pad=15)

charge_plot_line, = axes.plot(charge_data[0], charge_data[1], color='blue', marker='o', markevery=10, linewidth=2)
discharge_plot_line, = axes.plot(discharge_data[0], discharge_data[1], color='red', marker='o', markevery=10, linewidth=2)

charge_plot_line.set_label("Заряд конденсатора")
discharge_plot_line.set_label("Разряд конденсатора")
axes.legend(prop={"size":16}, loc='upper right')

x_limits = (0.0, math.ceil(time_max) + 1)
y_limits = (0.0, 3.5)
axes.set(xlim=x_limits, ylim=y_limits)

axes.yaxis.set_minor_locator(MultipleLocator(0.1))
axes.xaxis.set_major_locator(MultipleLocator(1.0))
axes.xaxis.set_minor_locator(MultipleLocator(0.1))
axes.yaxis.set_major_locator(MultipleLocator(0.5))


axes.grid(which='major', color='blue', linestyle='-', linewidth=0.3)
axes.grid(which='minor', color='blue', linestyle=':', linewidth=0.3)

charge_time = time_arr[volt_max_ind]
discharge_time = time_arr[-1] - time_arr[volt_max_ind]

axes.axvline(x=charge_time, ymin=0, ymax=volt_max/y_limits[1], color='green', linestyle='dashed')
axes.axhline(y=volt_max, xmin=0, xmax=charge_time/x_limits[1], color='green', linestyle='dashed')

axes.scatter(time_arr[volt_max_ind], volt_max, color='green', s=50)
axes.text(charge_time + 0.1, 0.05, f"{charge_time:.2f}", fontsize=12)
axes.text(0.1, volt_max + 0.05, f"{volt_max:.2f}", fontsize=12)

axes.text(charge_time + 3.0, 0.75 * volt_max, f"Время заряда: {charge_time:.2f} с\nВремя разряда: {discharge_time:.2f} с",
          color='black', fontsize=16)

figure.savefig("graph.svg")
