#!/usr/bin/env python3
import serial
import time

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('/dev/ttyACM0', 9800, timeout=1)
time.sleep(2)

filename="data_file.txt"
f = open("data_file.txt", "a")
 
while True:
    s    = ser.readline()
    line = s.decode('utf-8')
    f.write(line)    # Appends output to file
    time.sleep(.1)
