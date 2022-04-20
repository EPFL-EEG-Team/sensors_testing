#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import sys
import numpy as np

#https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8875677
# theta, alpha, beta_low
freq_ranges = [(4, 7), (8, 12), (13, 20)] 

#figure
fig, ax = plt.subplots(2,1, figsize=(5,10))
ax1 = ax[0]
ax2 = ax[1]
line1, = ax1.plot([],[],'b-')

length = 100
fftfreq = np.fft.fftfreq(length,d=10/1000) #data interval is 10ms
xdata = fftfreq[1:length//4]
data = np.zeros((length,))

#serial port
sensor = serial.Serial('COM3', 9600) #port name and baud
sensor.reset_input_buffer()
signal = sensor.readline()


def animate(i):
    #read in new data
    data[0:length-1] = data[1:length]
    signal = sensor.readline()
    [t, data[-1]] = [float(x) for x in signal.decode().split(',')]
    
    #fft
    amp=np.abs(np.fft.fft(data))**2
    pw = amp[1:length//4]/np.sum(amp[1:length//4])
    summary = [np.mean(pw[np.where((fftfreq>=x)&(fftfreq<=y))]) for (x, y) in freq_ranges]
   
    #replotting
    ax1.clear()
    ax1.plot(xdata, pw)

    ax1.set_xlabel('freq (Hz)')
    ax1.set_ylabel('Normalized Power')
    ax1.set_title("time %f"%(t/1000))	

    ax2.clear()
    ax2.bar(range(len(summary)), summary)

	
try:
    ani = animation.FuncAnimation(fig, animate, interval=1) 
    plt.show()
except KeyboardInterrupt:
    sensor.close()
    sys.exit()