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
bitwidth = 1
fbinwidth = 50
fmin = 100
fmax = 5000
Df = fmax-fmin

# Calculate scaling factor
tscale = 8.055/355227
vscale = 1/300000
ampscale = 2200

def get_bits(plot):
    
    # Create arrays
    bits = []
    a = read("strobe.wav")
    b = np.array(a[1],dtype=float)
    c = []
    for i in range(len(b)):
        c = np.append(c,b[i,1]*vscale)
    t = np.linspace(0, 8.055, len(b))
    
    # Plot V vs t
    if plot == 1:
        plt.figure()
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [V]')
        plt.title('Voltage as a function of time')
        #plt.xlim([0,0.05]) #comment out for graph of full data set
        plt.plot(t,b[:,1])
    
    # Remove leading noise before actual message
    
    
    # Create Power Spectrums
    for i in range(int(ttot/bitwidth-1)):
        f, Pxx_den = signal.periodogram(c[int(i/tscale):int((i+1)/tscale)], 1/tscale) #need subarray of c that contain's i'th bit
        maxj = 0
        for j in range(len(Pxx_den)):
            if j > 60 and Pxx_den[j] > Pxx_den[maxj]:
                maxj = j
        bit = round(f[maxj]/fbinwidth + 0.5)
        bit = bin(bit)
        bits = np.append(bits, bit)
    
    return bits


bits = get_bits(1)
for i in range(len(bits)):
    print(bits[i])