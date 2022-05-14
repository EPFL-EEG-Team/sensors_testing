#importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import sys
import numpy as np
from sklearn import svm

#Base line parameters
num_trials = 3
num_types = 2
list_types = ['Relax', 'Focus']
pred_types = ['Relax', 'Neutral', 'Focus']
num_iter_per_type = 40
baseline_frames = num_trials * num_types * num_iter_per_type

#Speed change
delta_speed = 1

#figure
fig, ax = plt.subplots(2,1, figsize=(5,10))
ax1 = ax[0]
ax2 = ax[1]
line1, = ax1.plot([],[],'b-')

length = 100
fftfreq = np.fft.fftfreq(length,d=2/1000)[1:10] #data interval is 10ms
data = np.zeros((length,))

#serial port
sensor = serial.Serial('COM3', 115200) #port name and baud
sensor.flushInput()
signal = sensor.readline()

num_samples = 10
fft_samples = np.zeros((len(fftfreq), num_samples))

#svm instance
svm_classifier = svm.SVC()
X = []
y = []

for i in range(num_samples):
    #read in new data
    sensor.flushInput()
    signal = sensor.readline()
    for j in range(length):
        signal = sensor.readline()
        [t, data[j]] = [float(x) for x in signal.decode().split(',')]
    
    #fft
    fft_samples[:, i] = np.log(np.abs(np.fft.fft(data))**2)[1:10]

mean = np.mean(fft_samples, axis=1)
std = np.std(fft_samples, axis=1)

ax1.clear()
ax1.plot(fftfreq, mean)
ax1.fill_between(fftfreq, mean+std, mean-std, alpha=0.25)
ax1.set_xlabel('freq (Hz)')
ax1.set_ylabel('log(power)')
ax1.set_title("time %.2f s"%(t/1000000))	

time_array = []
ind_array = []

def animate_baseline_aquire(i):
    mode = (i//num_iter_per_type)%num_types
    ax2.set_title(list_types[mode])
    ax2.set_xlabel(i)

    #read in new data
    sensor.flushInput()
    signal = sensor.readline()
    for j in range(length):
        signal = sensor.readline()
        [t, data[j]] = [float(x) for x in signal.decode().split(',')]
    
    #fft
    fft_samples[:, i%num_samples] = np.log(np.abs(np.fft.fft(data))**2)[1:10]

    mean = np.mean(fft_samples, axis=1)
    std = np.std(fft_samples, axis=1)

    if (i%num_iter_per_type)>=20:
        #X.append(fft_samples[:, i%num_samples])
        X.append(mean)
        if mode == 0:
            y.append(-1)
        else:
            y.append(1)

    #replotting
    ax1.clear()
    ax1.plot(fftfreq, mean)
    ax1.fill_between(fftfreq, mean+std, mean-std, alpha=0.25)
    ax1.set_ylim([5, 15])
    ax1.set_xlabel('freq (Hz)')
    ax1.set_ylabel('log(power)')
    ax1.set_title("time %.2f s"%(t/1000000))
    
    
def animate(i):
    if i < baseline_frames:
        animate_baseline_aquire(i)
    elif i == baseline_frames:
        svm_classifier.fit(X, y)
    else:
        #read in new data
        sensor.flushInput()
        signal = sensor.readline()
        for j in range(length):
            signal = sensor.readline()
            [t, data[j]] = [float(x) for x in signal.decode().split(',')]
        
        #fft
        fft_samples[:, i%num_samples] = np.log(np.abs(np.fft.fft(data))**2)[1:10]

        mean = np.mean(fft_samples, axis=1)
        std = np.std(fft_samples, axis=1)

        pred = svm_classifier.predict([mean])[0]

        if len(ind_array)==0:
            speed = pred * delta_speed
        else:    
            speed = ind_array[-1] + pred * delta_speed

        if speed > 255:
            speed = 255
        elif speed < 0:
            speed = 0

        time_array.append(t/1000000)
        ind_array.append(speed)

        #replotting
        ax1.clear()
        ax1.plot(fftfreq, mean)
        ax1.fill_between(fftfreq, mean+std, mean-std, alpha=0.25)
        ax1.set_ylim([5, 15])
        ax1.set_xlabel('freq (Hz)')
        ax1.set_ylabel('log(power)')
        ax1.set_title("time %.2f s"%(t/1000000))	

        ax2.clear()
        ax2.plot(time_array, ind_array)
        ax2.set_title(pred_types[pred+1])
        ax2.set_ylabel('Speed')
	
try:
    ani = animation.FuncAnimation(fig, animate, interval=0) 
    plt.show()
except KeyboardInterrupt:
    plt.close()
    sensor.close()
    sys.exit()