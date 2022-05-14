#importing libraries
import numpy as np
from sklearn import svm

#Global Parameters and Variables
#Base line parameters
list_types = ['Relax', 'Focus']
num_trials = 3
num_iter_per_type = 40
baseline_frames = num_trials * len(list_types) * num_iter_per_type

#Speed change delta
delta_speed = 1

#fft related
length = 100
fftfreq = np.fft.fftfreq(length,d=2/1000)[1:10] #data interval is 2ms

num_samples = 10 #number of frames for mean
fft_samples = np.zeros((len(fftfreq), num_samples))

#svm instance
svm_classifier = svm.SVC()
X = []
y = []

#Speed array
speed_array = []

def baseline_acquisition(i, data):
    mode = (i//num_iter_per_type)%len(list_types)
    print("Base line acquisition: " + list_types[mode], end="\r")
    
    #fft calculation
    fft_samples[:, i%num_samples] = np.log(np.abs(np.fft.fft(data))**2)[1:10]

    #Only use latter half of the data
    if (i%num_iter_per_type)>=num_iter_per_type//2:
        mean = np.mean(fft_samples, axis=1)
        X.append(mean)
        y.append(mode)
    
    speed_array.append(0)
    
    
def get_speed(data):
    assert data.shape==(length,), "data size does not match"
    
    i = len(speed_array)
    
    #When the base line data acquisition is done
    #Train svm
    if i == baseline_frames:
        svm_classifier.fit(X, y)
        print("Base line done!", end="\r")
    
    #At first ground truth data collection
    if i < baseline_frames:
        baseline_acquisition(i, data)
    else:    
        #fft calculation
        fft_samples[:, i%num_samples] = np.log(np.abs(np.fft.fft(data))**2)[1:10]
        mean = np.mean(fft_samples, axis=1)

        #Obtain the prediction and update speed
        pred = svm_classifier.predict([mean])[0]
        if pred == 0:
            speed = speed_array[-1] - delta_speed
        else:
            speed = speed_array[-1] + delta_speed

        #Limit the range of the speed (0 to 255 inclusive)
        if speed > 255:
            speed = 255
        elif speed < 0:
            speed = 0

        speed_array.append(speed)
        print("Current state: " + list_types[pred] + ", Speed: " + str(speed), end= "\r")

    return speed_array[-1]


