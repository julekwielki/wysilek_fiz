# Na podstawie 12 kanałowych zapisów EKG rejestrowanych podczas wysiłku na ergometrze rowerowym wyznacz czasy trwania
# interwałów RR. Przedstaw rekomendacje dotyczące wstępnej obróbki sygnałów EKG i oceny występowania artefaktów.
# Którego kanału użyłbyś/użyłabyś do wyznaczania rytmu serca?

from tkinter import filedialog
import wfdb as wfdb
from matplotlib import pyplot as plt
from numpy import *
import neurokit2 as nk

# """
file = filedialog.askopenfilename(initialdir=".", filetypes=[("Plik DAT", "*.dat")])  # wczytanie z pliku, potrzebny dodatkowy plik .hea z informacjami
filename = str(file)
name = filename[0:len(filename)-4]
print(name)
# """

# name = "132022-2023-04-27-10-44-55_MG_ramp"  # przykładowe pliki
# name = "132022-2023-05-19-09-50-04_MG_const"

ecg_data_raw = wfdb.rdrecord(name)
fs = 500  # nie wiem, ale wydaje się w miarę ok

zapis = []

for i in range(len(ecg_data_raw.p_signal[0])):
    dane = []
    for a in range(len(ecg_data_raw.p_signal)):
        dane.append(ecg_data_raw.p_signal[a][i])
    zapis.append(dane)

print(len(zapis[0]))
x = [i/fs for i in range(len(zapis[0]))]
print(len(x))

# """   # wszystkie 12 zapisów na jednym wykresie
fig, axes = plt.subplots(3, 4)
minn, maxx = 80, 1400
for i in range(len(axes)):
    for j in range(len(axes[0])):
        axes[i][j].plot(x[minn:maxx], zapis[j + i * 4][minn:maxx])
        axes[i][j].set_title("lead " + str(j + i * 4 + 1) + "?") 
fig.set_size_inches(15, 10, forward=True)
fig.savefig(name +" 16 .png")
# plt.show()

# """
nr = 0
"""  # analiza zapisu korzystając z gotowego pakietu do wykresu
minn, maxx = 80, 5000  # zakres bo inaczej jest średio czytelny wykres
signals, info = nk.ecg_process(zapis[nr], fs)
nk.ecg_plot(signals, info)
fig = plt.gcf()
fig.set_size_inches(10, 12, forward=True)
fig.savefig("32 " + name + " " + str(nr) +" cale.png")
# """
