# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:01:50 2019

@author: Nick
"""

from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

# Constants
ttot = 5

# Variables
fmin = 100
fmax = 5000
Df = fmax-fmin

# Calculate scaling factor
tscale = 8.055/355227
vscale = 1/300000
ampscale = 2200

def get_bits(plot):
    
    # Create arrays
    a = read("test15.wav")
    b = np.array(a[1],dtype=float)
    t = np.linspace(0, 8.055, len(b))
    
    # Scale
    for i in range(len(b)):
        b[i,0] = b[i,0]*vscale
        b[i,1] = b[i,1]*vscale
        
    # Create Power Spectrum
    f, Pxx_den = signal.periodogram(b[:,0], 1/tscale)
    fArray = [100,150,200,250]
    bitArray = []
    
    ind = np.argmax(Pxx_den)
    for k in range (len(fArray)):
        if (f[ind]<fArray[k]+2) and (f[ind]>fArray[k]-2):
            bitArray.append(bin(fArray[k]))        
    
    print(bitArray)
    
    # Plot
    if plot == 1:
        plt.figure()
        plt.get_current_fig_manager().window.showMaximized()
        
        # Plot V vs t
        plt.subplot(2,1,1)
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [V]')
        plt.title('Voltage as a function of time')
        #plt.xlim([0,0.05]) #comment out for graph of full data set
        plt.plot(t,b[:,0])
        
        # Plot Power Spectrum
        plt.subplot(2,1,2)
        plt.xlabel('frequency [Hz]')
        plt.ylabel('PSD [V**2/Hz]')
        plt.title('Power Spectrum')
        #plt.xlim([0,1000]) #comment out for graph of full data set
        #plt.ylim([10e-8,10e-2]) #comment out for graph of full data set
        plt.plot(f, Pxx_den)
        
get_bits(1)