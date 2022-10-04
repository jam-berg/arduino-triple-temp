#!/usr/bin/env python3
import serial
import csv

arduino_port = "/dev/cu.usbmodem14201" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
fileName="analog-data.csv" #name of the CSV file generated


ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "a")
print("Created file")

#display the data to the terminal
getData=ser.readline()
dataString = getData.decode('utf-8')
data=dataString[0:][:-2]
print(data)

readings = data.split(",")
print(readings)

sensor_data.append(readings)
print(sensor_data)


samples = 3 #how many samples to collect
print_labels = False
line = 0 #start at 0 because our header is 0 (not real data)
sensor_data = [] #store data

# collect the samples
while line <= samples:
    getData=ser.readline()
    dataString = getData.decode('utf-8')
    data=dataString[0:][:-2]
    print(data)

    readings = data.split(",")
    print(readings)

    sensor_data.append(readings)
    print(sensor_data)

    line = line+1
