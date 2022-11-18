#!/usr/bin/env python3

from datetime import datetime
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import math
now = datetime.now()
current_time = now.strftime("%d_%m_%y_%H_%M_%S")
print("Current Time =", current_time)

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

filename = "data_file_" + current_time + ".txt"
#f = open(filename, "a")

# defs für Auswertung
cyclezeit = 45
anzahlcycles = 2
basetemperature = 0
material="pom"


#dichte & wärmeleitzahl der Matterialien
if material == "pmma":
    d=1180
    c=1470
if material=="pom":
    d=1410
    c=1500
if material=="nylon":
    d=1084
    c=1700

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
        #f.write(line)  # Appends output to file

        a.append(line[:-2])

        time.sleep(0.1)

    b.append(a)

    a = []

result = []
cycles = []


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

ergebnis=[]

yachsed=[]
xachsed=[]
qergebnis=[]
thetaergebnis=[]


fig=plt.figure(figsize=(9.5,4.5))
ax1=fig.add_subplot(121)
ax2=fig.add_subplot(122)


for u in range(1, anzahlcycles):
    X0 = (max(daten[liste[2 * u]])-min(daten[liste[2*u]]))/2
    Y0 = (max(daten[liste[2 * u + 1]])-min(daten[liste[2 * u + 1]]))/2
    y_distance_index = find_index_nearest_to_0(daten[liste[2 * u]])
    y_distance_to_0 = daten[liste[2 * u + 1]][y_distance_index]
    miny0=min(daten[liste[2 * u + 1]])
    distance_y_to_0=Y0-(y_distance_to_0-miny0)

    #print(X0)
    #print(Y0)
    #print(distance_y_to_0)

    q=X0/Y0
    theta=np.arcsin(distance_y_to_0/Y0)
    T=cyclezeit
    D=(np.pi*0.000001)/(T*theta*math.log(X0/Y0,math.e))

    yachsed.append(Y0)
    xachsed.append(X0)
    qergebnis.append(q)
    thetaergebnis.append(theta)

    lambdaeinzel=D*c*d

    ergebnis.append(lambdaeinzel)
    ax1.plot(daten[liste[2 * u]], daten[liste[2 * u + 1]], marker=".", linestyle=" ", label=str(u))



'''

print(X0)
print(Y0)
print(qergebnis)
print(thetaergebnis)

'''
f=0
for i in ergebnis:
    f+=i


wärmeleitfähigkeit=f/len(ergebnis   )
print(ergebnis)
print(wärmeleitfähigkeit)


ax2.plot(ergebnis)
ax2.plot(wärmeleitfähigkeit)

plt.title(material)
plt.legend()
plt.savefig("data_file_" + current_time + ".png")
plt.show()
