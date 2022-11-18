#!/usr/bin/env python3

from datetime import datetime
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm
now = datetime.now()
current_time = now.strftime("%d_%m_%y_%H_%M_%S")
print("Current Time =", current_time)

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

filename = "data_file_" + current_time + ".txt"
f = open(filename, "a")

# defs für Auswertung
cyclezeit = 42
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
    return (np.abs(array).argmin())

def find_index_nearest_to_value(array, value):
    array = np.asarray(array)
    return (np.abs(array - value).argmin())

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


for i in b:
    for j in i:
        element = j.split(";")
        element.pop(0)
        for u in element:
            result.append(float(u) - basetemperature)

    cycles.append(result)
    result = []

liste = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
daten = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0}

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
    x_values = daten[liste[2 * u]]
    y_values = daten[liste[2 * u + 1]]
    x_values_max = max(x_values)
    x_values_min = min(x_values)
    y_values_max = max(y_values)
    y_values_min = min(y_values)

    X0 = (x_values_max - x_values_min) / 2
    Y0 = (y_values_max - y_values_min) / 2
    mittelpunkt = [x_values_min + X0, y_values_min + Y0]
    print(mittelpunkt[0])
    print(mittelpunkt[1])

    y_distance_index = find_index_nearest_to_value(x_values, x_values_min + X0)
    y_distance_to_0 = y_values[y_distance_index]
    print(y_distance_to_0,"y wert senkrecht zu mittelpunkt")

    distance_y=abs(mittelpunkt[1] - y_distance_to_0)
    print(distance_y)
    print(Y0)
    #print(X0)
    #print(Y0)
    #print(distance_y_to_0)

    q=X0/Y0
    theta=np.arcsin(distance_y/Y0)
    T=cyclezeit
    theta_grad=theta*360/(2*np.pi)
    D=(np.pi*0.000001)/(T*theta_grad*math.log(X0/Y0,math.e))

    yachsed.append(Y0)
    xachsed.append(X0)
    qergebnis.append(q)
    thetaergebnis.append(theta)

    lambdaeinzel=D*c*d

    ergebnis.append(lambdaeinzel)
    ax1.plot(x_values, y_values, marker=".", linestyle=" ", label=str(u))





print(X0,"X0")
print(Y0,"Y0")
print(qergebnis,"q")
print(thetaergebnis,"theta")

f=0
erhalt=[]
for i in ergebnis:
    f+=i



wärmeleitfähigkeit=f/len(ergebnis )

print(ergebnis)
print(wärmeleitfähigkeit)


mu, std = norm.fit(ergebnis)

# Plot the histogram.
'''
zum einfügen
density=1
'''
ergebnis_normalized = np.divide(ergebnis, f)
ax2.hist(ergebnis_normalized,density=1, alpha=0.6, color='g')

# Plot the PDF.
xmin=min(ergebnis)
xmax=max(ergebnis)
x = np.linspace(xmin, xmax, 100)
#p= (np.pi*std) * np.exp(-0.5*((x-mu)/std)**2)
p = norm.pdf(x, mu, std)
ax2.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)




plt.savefig("data_file_" + current_time + ".png")
plt.show()
