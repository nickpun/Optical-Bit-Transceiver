# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:34:54 2019

@author: Nick
"""

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

fs = 10e3
N = 1e5
amp = 0.2*np.sqrt(2)
freq = 123.0
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

f, Pxx_den = signal.periodogram(x, fs)


fig, ax = plt.subplots(1,1)
ax.semilogy(f, Pxx_den)
#ax.set_ylim([0.0001, 0.5])
#ax.set_xlim([122, 124])
#ax.set_xlim([1,500])
ax.set_xlabel('frequency [Hz]')
ax.set_ylabel('PSD [V**2/Hz]')


#fig2, ax2=plt.subplots(1,1)
#ax2.plot(time,x)
#ax2.set_xlim([0, 0.1])