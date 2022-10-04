#!/usr/bin/env python3
from datetime import datetime
import serial
import time


now = datetime.now()
current_time = now.strftime("%d_%m_%y_%H_%M_%S")
print("Current Time =", current_time)


# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('/dev/ttyACM0', 9800, timeout=1)
time.sleep(2)

filename="data_file_" + current_time + ".txt"
f = open(filename, "a")
 
while True:
    s    = ser.readline()
    line = s.decode('utf-8')
    print(line)
    f.write(line)    # Appends output to file
    time.sleep(.1)
