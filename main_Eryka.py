
# Na podstawie 12 kanałowych zapisów EKG rejestrowanych podczas wysiłku na ergometrze rowerowym wyznacz czasy trwania
# interwałów RR. Przedstaw rekomendacje dotyczące wstępnej obróbki sygnałów EKG i oceny występowania artefaktów.
# Którego kanału użyłbyś/użyłabyś do wyznaczania rytmu serca?

from tkinter import filedialog
import numpy as np
import neurokit2 as nk
import wfdb as wfdb
from matplotlib import pyplot as plt
from numpy import *
import pandas as pd
from neurokit2 import signal_rate, signal_sanitize, signal_filter
from neurokit2 import ecg_delineate
from neurokit2 import ecg_peaks
from neurokit2 import ecg_phase
from neurokit2 import ecg_quality


def EL_ecg_process(ecg_signal, sampling_rate=500, method="neurokit", lf=0, hf=0, pl=0, FilterType = "butterworth", FilterOrder = 5):
    # Sanitize and clean input
    ecg_signal = signal_sanitize(ecg_signal)
    ecg_cleaned = ecg_signal
    if lf != 0:
        ecg_cleaned = signal_filter(ecg_cleaned, lowcut=lf, method=FilterType, order=FilterOrder, sampling_rate=sampling_rate)

    if hf != 0:
        ecg_cleaned = signal_filter(ecg_cleaned, highcut=hf, method=FilterType, order=FilterOrder, sampling_rate=sampling_rate)

    if pl != 0:
        ecg_cleaned = signal_filter(ecg_cleaned, method="powerline", powerline=pl, sampling_rate=sampling_rate)

    # Detect R-peaks
    instant_peaks, info = ecg_peaks(
        ecg_cleaned=ecg_cleaned,
        sampling_rate=sampling_rate,
        method=method,
        correct_artifacts=True,
    )

    # Calculate heart rate
    rate = signal_rate(
        info, sampling_rate=sampling_rate, desired_length=len(ecg_cleaned)
    )

    # Assess signal quality
    quality = ecg_quality(
        ecg_cleaned, rpeaks=info["ECG_R_Peaks"], sampling_rate=sampling_rate
    )

    # Merge signals in a DataFrame
    signals = pd.DataFrame(
        {
            "ECG_Raw": ecg_signal,
            "ECG_Clean": ecg_cleaned,
            "ECG_Rate": rate,
            "ECG_Quality": quality,
        }
    )

    # Delineate QRS complex
    delineate_signal, delineate_info = ecg_delineate(
        ecg_cleaned=ecg_cleaned, rpeaks=info["ECG_R_Peaks"], sampling_rate=sampling_rate
    )
    info.update(delineate_info)  # Merge waves indices dict with info dict

    # Determine cardiac phases
    cardiac_phase = ecg_phase(
        ecg_cleaned=ecg_cleaned,
        rpeaks=info["ECG_R_Peaks"],
        delineate_info=delineate_info,
    )

    # Add additional information to signals DataFrame
    signals = pd.concat(
        [signals, instant_peaks, delineate_signal, cardiac_phase], axis=1
    )

    # return signals DataFrame and R-peak locations
    return signals, info


# name = "132022-2023-04-27-10-44-55_MG_ramp"  # przykładowe pliki
name = "132022-2023-05-19-09-50-04_MG_const"
name = "142023-2023-05-25-10-46-16_MK_ramp"
'''
file = filedialog.askopenfilename(initialdir=".", filetypes=[("Plik DAT", "*.dat")])  # wczytanie z pliku, potrzebny dodatkowy plik .hea z informacjami
filename = str(file)
name = filename[0:len(filename)-4]
print(name)
#'''

minn, maxx = 25000, 425000  # do tworzenia wykresów
#minn, maxx = 250, 4250 # do testów
# Pan & Tompkins (1985)
Lowfreq = 0.5  # domyslnie 5
#0.5 1 5
Highfreq = 15  # domyslnie 15
#0 10 15 20
PoweLine = 50  # domyslnie 50
#0 50
FilterType = "butterworth_zi"  #"bessel" # butterworth_zi
FilterOrder = 1

ecg_data_raw = wfdb.rdrecord(name)
fs = 500

zapis = []

for i in range(len(ecg_data_raw.p_signal[0])):
    dane = []
    for a in range(len(ecg_data_raw.p_signal)):
        dane.append(ecg_data_raw.p_signal[a][i])
    zapis.append(dane)

print(len(zapis[0]))
x = [i/fs for i in range(len(zapis[0]))]
print(len(x))
print(x[-1]/60)
minn, maxx = 92000, 95000  # 100000  # len(x)
"""   # wszystkie 12 zapisów na jednym wykresie
fig, axes = plt.subplots(3, 4)
for i in range(len(axes)):
    for j in range(len(axes[0])):
        axes[i][j].plot(x[minn:maxx], zapis[j + i * 4][minn:maxx])
        axes[i][j].set_title("lead " + str(j + i * 4 + 1))
plt.show()
# """

# plt.plot(x[minn:maxx], zapis[1][minn:maxx])
# plt.plot(zapis[1][minn:maxx])
# plt.show()

ecg_signal = signal_sanitize(zapis[1])
ecg_cleaned = ecg_signal
lf, hf, pl = 0.5, 0, 0
FilterType = "butterworth"
FilterOrder = 2
if lf != 0:
    ecg_cleaned = signal_filter(ecg_cleaned, lowcut=lf, method=FilterType, order=FilterOrder, sampling_rate=fs)

if hf != 0:
    ecg_cleaned = signal_filter(ecg_cleaned, highcut=hf, method=FilterType, order=FilterOrder, sampling_rate=fs)

if pl != 0:
    ecg_cleaned = signal_filter(ecg_cleaned, method="powerline", powerline=pl, sampling_rate=fs)

plt.plot(x[minn:maxx], zapis[1][minn:maxx], label='unfiltered')
plot_name = "lf= " + str(lf) + ", hf= " + str(hf) + ", pl= " + str(pl)
plt.plot(x[minn:maxx], ecg_cleaned[minn:maxx], label=plot_name)
# plt.plot(zapis[1][minn:maxx])
plt.legend()
plt.show()
"""
signals, info = EL_ecg_process(zapis[1][minn:maxx], fs)
nk.ecg_plot(signals, info)
fig = plt.gcf()
fig.set_size_inches(10, 12, forward=True)
fig.savefig("myfig2.png")
signals.plot(subplots=True)
#"""
'''
print(len(zapis))
result = re.search('_(.*)dat', name)
print(result.group(1))
'''
name = name[27:]
print(name)
'''
for i in range(len(zapis)):
    fig1name = str(name) + '_ch' + str(i) + '_lf' + str(Lowfreq) + '_hf' + str(Highfreq) + '_pl' + str(PoweLine) +'_'+ FilterType+str(FilterOrder) + ".png"
    signals, info = EL_ecg_process(zapis[i][minn:maxx], fs, lf=Lowfreq, hf=Highfreq, pl=PoweLine, FilterType = FilterType, FilterOrder = FilterOrder)
    nk.ecg_plot(signals, info)
    fig = plt.gcf()
    fig.set_size_inches(10, 12, forward=True)
    fig.savefig("./Obrazki/"+fig1name)
#'''

#plt.show()
