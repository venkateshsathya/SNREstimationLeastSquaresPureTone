#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:34:18 2020

@author: venkat
"""


import numpy as np
#IQ_val = read_file('SIgnGenTRansmit900pt05_minus61pt5dBm1sec_trial1.bin');

filelocation = '/Users/venkat/Documents/ModulationClassificationOTA/pythonFiles/'
filename = filelocation + 'SIgnGenTRansmit900pt05_minus56pt5dBm1sec_trial1.bin'

with open(filename, 'rb') as fid:
        data_array = np.fromfile(fid, '<f4')
        

IQ_realwhole = data_array[0::2]
IQ_imagwhole = data_array[1::2]
        
        
offset=2*np.power(10,5)
IQ_real = IQ_realwhole[offset : offset+np.power(10,3)]
IQ_imag = IQ_imagwhole[offset : offset+np.power(10,3)]
fc = 50e3
fs = 2.5e6
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
amp_start = 0.8
amp_end = 1.2
amp_step = 0.05 # %0.01
freq_start = fc-200
freq_end = fc+200
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
real_error_val_fine = np.zeros((len1,len2,len3))
imag_error_val_fine = np.zeros((len1,len2,len3))

for a_val in np.arange(amp_start,amp_end+amp_step,amp_step):
    
    j=0
    for freq_val in np.arange(freq_start,freq_end + freq_step, freq_step):
       
       k=0
       for phase_val in np.arange(phase_start,phase_end+phase_step,phase_step):
         
         #a_val
         signal_estimate = a_val*np.cos(2*np.pi*freq_val*ts*range(1,N+1,1) + phase_val)
         real_error_val[i,j,k] = np.mean(np.power((IQ_real_norm - signal_estimate),2))
         imag_error_val[i,j,k] = np.mean(np.power((IQ_imag_norm - signal_estimate),2))
         k=k+1
       j=j+1
    i=i+1

