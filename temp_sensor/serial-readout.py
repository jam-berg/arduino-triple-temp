#!/usr/bin/env python3

from datetime import datetime
import serial
import time
import matplotlib.pyplot as plt
import numpy as np

now = datetime.now()
current_time = now.strftime("%d_%m_%y_%H_%M_%S")
print("Current Time =", current_time)

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

filename = "data_file_" + current_time + ".txt"
f = open(filename, "a")

# defs für Auswertung
cyclezeit = 45
anzahlcycles = 1
basetemperature = 0

a = []
b = []
t_finish = time.time() + cyclezeit * anzahlcycles

def find_index_nearest_to_0(array):
    array = np.asarray(array)
    return (np.abs(array)).argmin()

while time.time() < t_finish:
    t_end = time.time() + cyclezeit
    while time.time() < t_end:
        s = ser.readline()
        line = s.decode('utf-8')
        print(line[:-2])
        f.write(line)  # Appends output to file

        a.append(line[:-2])

        time.sleep(0.1)

    b.append(a)

    a = []

result = []
cycles = []
print(len(b))

for i in b:
    for j in i:
        element = j.split(";")
        element.pop(0)
        for u in element:
            result.append(float(u) - basetemperature)

    cycles.append(result)
    result = []

liste = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
daten = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0}

ja = []
nein = []

for u in range(len(cycles)):
    for i in range(1, len(cycles[u]), 3):
        ja.append(cycles[u][i])
    for j in range(2, len(cycles[u]), 3):
        nein.append(cycles[u][j])
    daten[liste[2 * u]] = ja
    daten[liste[2 * u + 1]] = nein
    ja = []
    nein = []

for u in range(0, anzahlcycles):
    X0 = (max(daten[liste[2 * u]])-min(daten[liste[2*u]]))/2
    Y0 = (max(daten[liste[2 * u + 1]])-min(daten[liste[2 * u + 1]]))/2
    y_distance_index = find_index_nearest_to_0(daten[liste[2 * u]])
    y_distance_to_0 = daten[liste[2 * u + 1]][y_distance_index]
    print(X0)
    print(Y0)
    print(y_distance_to_0)

    plt.plot(daten[liste[2 * u]], daten[liste[2 * u + 1]], marker="x", linestyle=" ")

# plt.plot(daten["A"],daten["B"], color = "k")
# plt.plot(daten["C"],daten["D"], marker = "x", color = "b", linestyle = " ")

plt.savefig("data_file_" + current_time + ".png")
plt.show()
