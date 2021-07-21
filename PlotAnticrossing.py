import tkinter as tk
from tkinter import filedialog

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import ReadSpectra as rs
import scipy.constants as cnst
import scipy.optimize as opt

"""
Fenster erstrellen, Spektrumdatei auswählen und Datei mit den Fitpunkten aus Plotspectrum.py auswählen
"""

root = tk.Tk()
root.withdraw()

datfile = filedialog.askopenfilename(
    title="Choose the .dat file.", filetypes=(("Data files", "*.dat"),)
)
fitdatafile = filedialog.askopenfilename(
    title="Choose the fitdata file.",
)

(intensity, xaxis, xaxis2, yaxis, eV) = rs.rspec(datfile)


label_colorscale = "Log10(Intensität)"
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlabel("Biasspannung [V]",fontsize=16)
ax.set_ylabel("Energie  [eV]",fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=14)
plt.tight_layout()

im = ax.imshow(
    intensity,
    norm=colors.SymLogNorm(0.5, linscale=0.05, base=10),
    cmap="Greys",
    aspect="auto",
    extent=[xaxis[0], xaxis[-1], eV[-1], eV[0]],
)

"""
Fitfunktionen definieren
"""
def Ep(x, E, p, d, g):
    return E+0.5*d - 0.5 * p * x + 0.5 * np.sqrt(( p * x-d) ** 2 + (2 * g) ** 2)


def Em(x, E, p, d, g): 
    return E+0.5*d - 0.5 * p * x - 0.5 * np.sqrt((p * x-d) ** 2 + (2 * g) ** 2)


"""
Daten der Fitpunkte auslesen
"""

linedata = np.loadtxt(fitdatafile)

epindex = np.argwhere(linedata[:, 0] > 0)
emindex = np.argwhere(linedata[:, 0] < 0)
epdata = np.hstack((linedata[epindex, 0],linedata[epindex, 1]))
emdata = np.hstack((np.abs(linedata[emindex, 0]),linedata[emindex,1]))
print(epdata.shape)
epdata = np.flip(epdata, 0)
emdata = np.flip(emdata, 0)

Emin = np.max([np.min(emdata[:, 0]), np.min(epdata[:, 0])])
Emax = np.min([np.max(emdata[:, 0]), np.max(epdata[:, 0])])


"""
Auswählen der Startparameter der Fitfunktionen
"""

if epdata[0, 1] > epdata[-1, 1]:
    psign = -1
else:
    psign = 1


xlspace = np.linspace(Emin, Emax, 100)
epinterp = np.interp(xlspace, epdata[:, 0], epdata[:, 1])
eminterp = np.interp(xlspace, emdata[:, 0], emdata[:, 1])
diff = epinterp - eminterp
g = 0.5 * np.min(diff)
linindex = epdata.size // 5
if psign == -1:
    p = -1 * np.polyfit(epdata[0:linindex, 0], epdata[0:linindex, 1], 1)[0]
else:
    p = -1 * np.polyfit(epdata[-linindex:-1, 0], epdata[-linindex:-1, 1], 1)[0]


d = xlspace[np.argmin(diff)]/p

E0 = 0.5 * (epinterp[np.argmin(diff)] + eminterp[np.argmin(diff)])



"""
Fitten der Funktionen
"""

def fitfunc(x, E, p, d, g):
    return [*Em(-x[x < 0], E, p, d, g), *Ep(x[x >= 0], E, p, d, g)]


fitx = np.concatenate((-1 * emdata[:, 0], epdata[:, 0]))
fity = np.concatenate((emdata[:, 1], epdata[:, 1]))
popt, pcov = opt.curve_fit(fitfunc, fitx, fity, p0=[E0, p, d, g],bounds=([0,-np.inf,-np.inf,0],np.inf))


"""
Plotten des Fits und der Fitpunkte über das Spektrum
und Ausgabe der ermittelten Parameter
"""

plt.scatter(epdata[:, 0], epdata[:, 1],c="b",linewidths=2)

xlspacep = np.linspace(np.min(epdata[:, 0]), np.max(epdata[:, 0]), 100)
xlspacem = np.linspace(np.min(emdata[:, 0]), np.max(emdata[:, 0]), 100)


plt.scatter(emdata[:, 0], emdata[:, 1],c="g",linewidths=2)


print("gemeinsamer fit", popt)
print(np.sqrt(np.diag(pcov)))

plt.plot(xlspacep, Ep(xlspacep, *popt), "b",linewidth=2)
plt.plot(xlspacem, Em(xlspacem, *popt), "g",linewidth=2)


plt.show()
