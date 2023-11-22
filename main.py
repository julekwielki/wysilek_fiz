from tkinter import filedialog

import wfdb as wfdb
from matplotlib import pyplot as plt
from numpy import *
import csv

# """
file = filedialog.askopenfilename(initialdir=".", filetypes=[("Plik DAT", "*.dat")])
filename = str(file)
name = filename[0:len(filename)-4]
print(name)
# """

# name = "132022-2023-04-27-10-44-55_MG_ramp"

# """


# ecg_data_raw = wfdb.rdsamp("132022-2023-04-27-10-44-55_MG_ramp")
ecg_data_raw = wfdb.rdrecord(name)

"""
print(len(ecg_data_raw))
print(ecg_data_raw[1])
print(len(ecg_data_raw[0]))
print(len(ecg_data_raw[0][0]))

dane = [[], [], [], [], [], [], [], [], [], [], [], []]
for a in ecg_data_raw[0]:
    for x in range(len(a)):
        dane[x].append(a[x])
"""

zapis = []
# """
print(ecg_data_raw)
for i in range(len(ecg_data_raw.p_signal[0])):
    dane = []
    for a in range(len(ecg_data_raw.p_signal)):
        dane.append(ecg_data_raw.p_signal[a][i])
    zapis.append(dane)
freq = ecg_data_raw.fs
print(freq)
e = ecg_data_raw
print(e.n_sig)
print(e.fmt)
print(e.baseline)

print(len(zapis))
print(len(zapis[0]))

fig, axes = plt.subplots(3, 4)

for i in range(len(axes)):
    for j in range(len(axes[0])):
        axes[i][j].plot(zapis[j + i * 4][42:])
        axes[i][j].set_title("lead " + str(j + i * 4 +1))

plt.show()

# """

