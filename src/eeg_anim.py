#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import sys
import numpy as np


#https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8875677
# theta, alpha, beta_low
freq_ranges = [(4, 7), (8, 12), (13, 20), (21, 30)] 
freq_names = ["theta", "alpha", "beta(low)", "beta(high)"]

#figure
fig, ax = plt.subplots(2,1, figsize=(5,10))
ax1 = ax[0]
ax2 = ax[1]
line1, = ax1.plot([],[],'b-')

length = 500
fftfreq = np.fft.fftfreq(length,d=2/1000) #data interval is 10ms
xdata = fftfreq[1:31]
data = np.zeros((length,))

#serial port
sensor = serial.Serial('COM3', 115200) #port name and baud
sensor.flushInput()
signal = sensor.readline()

#base line measurement
base_trial = 10
baseline = np.zeros((len(fftfreq),))
for _ in range(base_trial):
    sensor.flushInput()
    signal = sensor.readline()
    for i in range(length):
        signal = sensor.readline()
        [t, data[i]] = [float(x) for x in signal.decode().split(',')]
    #fft
    amp=np.abs(np.fft.fft(data))**2
    baseline = baseline + amp
baseline = baseline / base_trial

def animate(i):
    #read in new data
    sensor.flushInput()
    signal = sensor.readline()
    for i in range(length):
        signal = sensor.readline()
        [t, data[i]] = [float(x) for x in signal.decode().split(',')]
    
    #fft
    amp=np.abs(np.fft.fft(data))**2
    pw = (amp - baseline)/ baseline
    summary = [np.mean(pw[np.where((fftfreq>=x)&(fftfreq<=y))]) for (x, y) in freq_ranges]
   
    #replotting
    ax1.clear()
    ax1.plot(xdata, pw[1:31])
    ax1.set_ylim([-5, 5])
    ax1.set_xlabel('freq (Hz)')
    ax1.set_ylabel('Relative change (%)')
    ax1.set_title("time %.2f s"%(t/1000000))	

    ax2.clear()
    ax2.bar(freq_names, summary)
    ax2.set_ylabel('Relative change (%)')
    ax2.set_ylim([-5, 5])

	
try:
    ani = animation.FuncAnimation(fig, animate, interval=1) 
    plt.show()
except KeyboardInterrupt:
    plt.close()
    sensor.close()
    sys.exit()