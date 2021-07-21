import tkinter as tk
from tkinter import filedialog

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import ReadSpectra as rs
import scipy.constants as cnst



"""
Fenster generieren, Spektrumdatei auswählen und Daten laden
"""

root = tk.Tk()
root.withdraw()


datfile = filedialog.askopenfilename(
    title="Choose the .dat file.", filetypes=(("Data files", "*.dat"),)
)
(intensity, xaxis, xaxis2, yaxis, eV) = rs.rspec(datfile)


"""
Plot des Spektrums mit Symlogskala (Logarithmische Skala mit linearen Anteil um Null)
"""

plt.rcParams.update({'font.size': 10})

label_colorscale = "Log10(Intensität)"
fig, ax = plt.subplots()
plt.tight_layout()
ax.set_xlabel("Spannung / Volt")
ax.set_ylabel("Energie / eV")

title = datfile.split("/")[-1]
title = title.split(".")[-2]
#fig.suptitle(title, fontsize=16)


im = ax.imshow(
    intensity,
    norm=colors.SymLogNorm(0.5, linscale=0.05, base=10),
    cmap="Greys",
    aspect="auto",
    extent=[xaxis[0], xaxis[-1], eV[-1], eV[0]],
)

xfitpoints = np.empty([1])
yfitpoints = np.empty([1])
fitpointsnum = int(0)




"""
Definition der Tastenbefehle
"""



shift_is_held = False
ctrl_is_held = False

def file_save(savedata):
    np.savetxt("fitdata.txt", savedata)

def on_key_press(event):
    global shift_is_held, ctrl_is_held, fitfunc, calcfit, xfitpoints, yfitpoints, plotfit
    if event.key == "shift":
        shift_is_held = True
    elif event.key == "control":
        ctrl_is_held = True
    elif event.key == "h":
        file_save(np.array([xfitpoints, yfitpoints]).transpose())
        print("file saved")


def on_key_release(event):
    global shift_is_held
    if event.key == "shift":
        shift_is_held = False
    elif event.key == "control":
        ctrl_is_held = False


"""
Fitpunkte für die obere Kurve Ep werden mit Shift+Linksklick, 
für die untere Kurve Em mit Strg+Linksklick ausgewählt
Die Fitpunkte werden in einem Array in einer txt Datei gespeichert.
Zur unterscheidung der Fitpunkte für Ep und Em
werden die Spannungswerte für Em mit einem negativen Vorzeichen versehen
"""

def onclick(event):
    global xfitpoints, yfitpoints, fitpointsnum, shift_is_held
    if shift_is_held:
        if fitpointsnum == 0:
            xfitpoints[0] = event.xdata
            yfitpoints[0] = event.ydata
        else:
            xfitpoints = np.append(xfitpoints, [event.xdata], 0)
            yfitpoints = np.append(yfitpoints, [event.ydata], 0)
        fitpointsnum = fitpointsnum + 1
    elif ctrl_is_held:
        if fitpointsnum == 0:
            xfitpoints[0] = -event.xdata
            yfitpoints[0] = event.ydata
        else:
            xfitpoints = np.append(xfitpoints, [-event.xdata], 0)
            yfitpoints = np.append(yfitpoints, [event.ydata], 0)
        fitpointsnum = fitpointsnum + 1


fig.canvas.mpl_connect("key_press_event", on_key_press)
fig.canvas.mpl_connect("key_release_event", on_key_release)

cid = fig.canvas.mpl_connect("button_press_event", onclick)


plt.show()
