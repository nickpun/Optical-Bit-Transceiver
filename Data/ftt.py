# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:15:56 2019

@author: Nick
"""

import numpy as np
import matplotlib.pyplot as plt

def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return (np.fft.ifft(f).real, f)

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    y = np.linspace(1,samples, samples)
    # idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    # f[idx] = 1
    f=10000/(10000+y*y)
    (noise,ft)=fftnoise(f)
    return (noise,ft)

(x,ft) = band_limited_noise(2, 200, 44100, 44100)
y = np.linspace(0,1, 44100)
fig, ax=plt.subplots(2,1)
ax[0].plot(x)
ax[1].plot(abs(ft)*abs(ft))
ax[1].set_xscale('log')
ax[1].set_yscale('log')