


#fps = 30
#sine_fq = 10 #Hz
#duration = 10 #seconds
#sine_5Hz = sine_generator(fps,sine_fq,duration)
#sine_fq = 1 #Hz
#duration = 10 #seconds
#sine_1Hz = sine_generator(fps,sine_fq,duration)

#sine = sine_5Hz + sine_1Hz




#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## This code computs the SNR from a pure tone received at a particular offset. 
# e need to specify the approximate frequency at which tone is expected and we search at  small region around it.
# We also o a search of ampitude and phase and by least squares aproach we get an SNR estimate. 

# the ttal sampls used for estimation is a hyper parameter and we have been using aroud 1000 o feew thousand to get a good estimate
#higher value might have fdifferenign freeq eror and thus impact SNR estimation.
import numpy as np
#IQ_val = read_file('SIgnGenTRansmit900pt05_minus61pt5dBm1sec_trial1.bin');
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import sys
import scipy.fftpack
#filelocation = '/home/gelu/Desktop/IQSamples/SNREstimate/'

fc = 50e3 # frequency offset from center frequency. Note that at baseband the IQ samples\
    #center frequency is 0Hz
fs = 1.25e6 # sampling rate used for capture

highpassfilter_cutoff = fc/2

def sine_generator(fs, sinefreq, duration):
    T = duration
    nsamples = fs * T
    w = 2. * np.pi * sinefreq
    t_sine = np.linspace(0, T, nsamples, endpoint=False)
    y_sine = np.sin(w * t_sine)
    result = pd.DataFrame({ 
        'data' : y_sine} ,index=t_sine)
    return result

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y
    
    
filename ='/home/gelu/Desktop/IQSamples/SNREstimate/BothUSRPSExternal10MhzSync_ToneCapture_1.bin' #sys.argv[1]

with open(filename, 'rb') as fid:
        data_array = np.fromfile(fid, '<f4')
        

IQ_realwhole_unfiltered = data_array[0::2]
IQ_imagwhole = data_array[1::2]

IQ_realwhole = butter_highpass_filter(IQ_realwhole_unfiltered,highpassfilter_cutoff,fs)

#plt.figure(figsize=(20,10))
#plt.subplot(211)
#plt.plot(IQ_realwhole_unfiltered)
#plt.title('generated signal')
#plt.subplot(212)
#plt.plot(IQ_realwhole)
#plt.title('filtered signal')
#plt.show()
#
#
#plt.figure(figsize=(20,10))
#plt.subplot(211)
#plt.plot(np.abs(scipy.fftpack.fft(IQ_realwhole_unfiltered)))
#plt.title('generated signal')
#plt.subplot(212)
#plt.plot(np.abs(scipy.fftpack.fft(IQ_realwhole)))
#plt.title('filtered signal')
#plt.show()
#
#print('Total number of samples in file is: ', len(IQ_realwhole))      
#offset=np.int(len(IQ_realwhole)/2)
total_samples_for_estimation = 10*np.power(10,3)
IQ_real = IQ_realwhole[offset : offset+total_samples_for_estimation]
IQ_imag = IQ_imagwhole[offset : offset+total_samples_for_estimation]

print('We are using the samples starting from ', offset,'. Total samples used for estimation is: ',total_samples_for_estimation)
      





print("Sampling rate used is: ", fs, " and the seed tone frequency used for search is: ", fc)
# fs = 1.25e6
ts = 1/fs
# IQ_val = read_file('.bin');
N = len(IQ_real)
##
#IQ_real = real(IQ_val)
#IQ_real = imag(IQ_val)

IQ_real_norm = IQ_real/np.max(IQ_real)
#IQ_real_norm =IQ_real_norm'
IQ_imag_norm = IQ_imag/np.max(IQ_imag)
#IQ_imag_norm = IQ_imag_norm'
amp_start = 0.5
amp_end = 1.2
amp_step = 0.05 # %0.01
freq_start = fc-400
freq_end = fc+400
freq_step = 20 # %0.2
phase_start = 0
phase_step = 2*np.pi/10 # %2*pi/360
phase_end = 2*np.pi

i=0
len1 = len(np.arange(amp_start,amp_end+amp_step,amp_step))
len2 = len(np.arange(freq_start,freq_end + freq_step, freq_step))
len3 = len(np.arange(phase_start,phase_end+phase_step,phase_step))
real_error_val = np.zeros((len1,len2,len3))
imag_error_val = np.zeros((len1,len2,len3))

print("COarse search space for amplitude is: ", amp_start," to ", amp_end, " in steps of :",amp_step)
print("COarse search space for frequency is: ", freq_start," to ", freq_end, " in steps of :",freq_step)
print("COarse search space for phase is: ", phase_start," to ", phase_end, " in steps of :", phase_step)
for a_val in np.arange(amp_start,amp_end+amp_step,amp_step):
    j=0
    for freq_val in np.arange(freq_start,freq_end + freq_step, freq_step):
       k=0
       for phase_val in np.arange(phase_start,phase_end+phase_step,phase_step): 
         #a_val
         #print(type(N))
         #temp1= 
         
         signal_estimate = a_val*np.cos(2*np.pi*freq_val*ts*range(1,np.int(N+1),1) + phase_val)
         real_error_val[i,j,k] = np.mean(np.power((IQ_real_norm - signal_estimate),2))
         imag_error_val[i,j,k] = np.mean(np.power((IQ_imag_norm - signal_estimate),2))
         k=k+1
       j=j+1
    i=i+1


#[mxv_real,idx] = min(real_error_val(:))
[i_real,j_real,k_real] = np.unravel_index(np.argmin(real_error_val),real_error_val.shape)

#[mxv_imag,idx] = min(imag_error_val(:));
[i_imag,j_imag,k_imag] = np.unravel_index(np.argmin(imag_error_val),imag_error_val.shape)


amp_range = np.arange(amp_start,amp_end+amp_step,amp_step)
freq_range = np.arange(freq_start,freq_end + freq_step, freq_step)
phase_range = np.arange(phase_start,phase_end+phase_step,phase_step)


true_amp_real_coarse = amp_range[i_real]
true_freq_real_coarse = freq_range[j_real]
true_phase_real_coarse = phase_range[k_real]

coarsesignal = true_amp_real_coarse*np.cos(2*np.pi*true_freq_real_coarse*ts*range(1,N+1,1) \
                                           + true_phase_real_coarse)
error_temp =  np.mean(np.power((IQ_real_norm - coarsesignal),2))
print('Least error estimated via coarse search is: ', error_temp, ' and via np.arg(real_error_val) \
      is: ', np.amin(real_error_val))

    
Coarse_SNR_estimate_real = 10*np.log10(np.mean(np.power(coarsesignal,2))/np.amin(real_error_val))
print("Coarse SNR Estimate is: ", Coarse_SNR_estimate_real)
#coarse_snr_estimates_array[snr_estimate_index] = Coarse_SNR_estimate_real
    
    
# Fine search

amp_start = true_amp_real_coarse-0.1
amp_end = true_amp_real_coarse+0.1
amp_step = 0.005 # %0.01
freq_start = true_freq_real_coarse-40
freq_end = true_freq_real_coarse+40
freq_step = 1 #0.2
phase_start = true_phase_real_coarse - 2*np.pi/10
phase_step = 2*np.pi/360 # %2*np.pi/360
phase_end = true_phase_real_coarse + 2*np.pi/10

len1 = len(np.arange(amp_start,amp_end+amp_step,amp_step))
len2 = len(np.arange(freq_start,freq_end + freq_step, freq_step))
len3 = len(np.arange(phase_start,phase_end+phase_step,phase_step))
real_error_val_fine = np.zeros((len1,len2,len3))
imag_error_val_fine = np.zeros((len1,len2,len3))


print("Fine search space for amplitude is: ", amp_start," to ", amp_end, " in steps of :",amp_step)
print("Fine search space for frequency is: ", freq_start," to ", freq_end, " in steps of :",freq_step)
print("Fine search space for phase is: ", phase_start," to ", phase_end, " in steps of :", phase_step)
    
    
i=0
for a_val in np.arange(amp_start,amp_end+amp_step,amp_step):
    print("i is: ", i)
    j=0
    for freq_val in np.arange(freq_start,freq_end + freq_step, freq_step):
       k=0
       
       for phase_val in np.arange(phase_start,phase_end+phase_step,phase_step): 
         #a_val
         #print(a_val,freq_val,phase_val)
         signal_estimate = a_val*np.cos(2*np.pi*freq_val*ts*range(1,N+1,1) + phase_val)
         #real_error_val_fine(i,j,k) = mean((IQ_real_norm - signal_estimate).^2);
         #imag_error_val_fine(i,j,k) = mean((IQ_imag_norm - signal_estimate).^2);
         real_error_val_fine[i,j,k] = np.mean(np.power((IQ_real_norm - signal_estimate),2))
         #imag_error_val_fine[i,j,k] = np.mean(np.power((IQ_imag_norm - signal_estimate),2))
         k=k+1
       j=j+1
    i=i+1

[i_real_fine,j_real_fine,k_real_fine] = np.unravel_index(np.argmin(real_error_val_fine)\
                                                         ,real_error_val_fine.shape)

min_error_power_real = np.amin(real_error_val_fine)
min_error_power_imag = np.amin(imag_error_val_fine)
amp_range = np.arange(amp_start,amp_end+amp_step,amp_step)
freq_range = np.arange(freq_start,freq_end + freq_step, freq_step)
phase_range = np.arange(phase_start,phase_end+phase_step,phase_step)

true_amp_real_fine = amp_range[i_real_fine]
true_freq_real_fine = freq_range[j_real_fine]
true_phase_real_fine = phase_range[k_real_fine]
print("true_freq_real_fine is: ",true_freq_real_fine)
real_fine_signal_estimate = true_amp_real_fine*np.cos(2*np.pi*true_freq_real_fine*ts*range(1,N+1,1) \
                                           + true_phase_real_fine)

SNR_estimate_real = 10*np.log10(np.mean(np.power(real_fine_signal_estimate,2))/min_error_power_real)
print("SNR Estimate is: ", SNR_estimate_real)

