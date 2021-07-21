"""
Formatiert die Messdateien für die Anderen Teilprogramme
"""

import pandas as pd

def rspec(datfile):
    data = pd.read_table(datfile, sep="\t", decimal=",", skiprows=[3])
    xaxis = data.iloc[0, 2:].to_numpy(dtype=float)
    xaxis2 = data.iloc[1, 2:].to_numpy(dtype=float)
    data2 = pd.read_table(datfile, sep="\t", decimal=",", skiprows=[1, 2, 3])
    yaxis = data2.iloc[0:, 1].to_numpy(dtype=float)
    yaxis2 = data2.iloc[0:, 0].to_numpy(dtype=float)
    intensity = data.iloc[2:, 2:].to_numpy(dtype=float)
    return (intensity, xaxis, xaxis2, yaxis, yaxis2)
