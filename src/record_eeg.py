#Script for recording serial data from arduino and put it into a csv file
import time
import serial
import csv
import sys

sensor = serial.Serial('COM3', 115200) #port name and baud
signal = sensor.readline()
filename = "eeg_" + time.strftime('%y-%m-%d-%H-%M-%S') + ".csv"
print("Recording to " + filename +"\n")
f = open(filename,'a', newline='')
wr=csv.writer(f)

try:
    while True:
        print("Recording " + time.strftime('%y-%m-%d %H:%M:%S'), end='\r')
        wr.writerow([int(x) for x in sensor.readline().decode().split(',')])
except KeyboardInterrupt:
    f.close()
    sensor.close()
    sys.exit()