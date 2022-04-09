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
freq = 200
kB = 1.38e-23
T0 = 293

# Variables
pltgrph = -1
fmin = 100
fmax = 5000
Df = fmax-fmin

# Calculate scaling factor
tscale = 8.055/355227
vscale = 1/300000
ampscale = 2200

#Rarr = [12,51,199,300,559,1795,2702,2998,3300,3900,6750,11990,14990,17950,
#        27040,30000,38790,55800,120000,179600,199400,270700,301800,392200]
Rarr = [12,51,199,300,559,1795,2702,3300,3900,6750,11990,14990,
        27040,30000,38780,38790,55800,120000,199400,270700,301800,392200,392201]

def Vtheory(R,T):
    return (4*kB*T*R*Df)**0.5

def main(R,plot,analysis):
    
    # Initiate arrays
    a = read("Johnson {0}Ohm.wav".format(R))
    b = np.array(a[1],dtype=float)
    
    # Variables
    Vhyp = Vtheory(R,T0)
    
    # Functions
    
    # Declare time array
    t = np.linspace(0, 8.055, len(b))
    
    # Scale
    for i in range(len(b)):
        b[i,0] = b[i,0]*vscale
        b[i,1] = b[i,1]*vscale
    
    # Plot V vs t
    if plot == pltgrph:
        plt.figure()
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [V]')
        plt.title('Voltage as a function of time')
        plt.xlim([0,0.05]) # comment out for graph of full data set
        plt.plot(t,b[:,1])
    
    # Create Power Spectrum
    f, Pxx_den = signal.periodogram(b[:,1], 1/tscale)
    
    # Plot Power Spectrum
    if plot == pltgrph:
        fig, ax = plt.subplots(1,1)
        ax.semilogy(f, Pxx_den)
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('PSD [V**2/Hz]')
        ax.set_title('Power Spectrum')
        plt.xlim([100,5000])
        plt.ylim([1e-10,1e-8])
    
    # Integrate
    df = f[1]-f[0]
    Vsqr = 0
    for i in range(len(Pxx_den)):
        if f[i] > fmax:
            break
        elif f[i] >= fmin:
            Vsqr += Pxx_den[i]*df
            
    # Calculations
    V = np.sqrt(Vsqr)/ampscale
    kBm = V**2/4/T0/R/Df
    
    # Analysis
    if analysis == 1:
        print('R = {0} Ohm'.format(R))
        print('Measured:')
        print('V_m = {0} V'.format(V))
        print('Theoretical:')
        print('V_t = {0} V'.format(Vhyp))
        print('V_m/V_t = {0}'.format(V/Vhyp))
        print('kBm = {0}'.format(kBm))
        print('')
        
        
    # Chi2
    
    output = [V,kBm]
    return output


# Iterate through each file
kBm = 0
size = 0
Varr = []
Rval = []

for i in range(len(Rarr)):
    if i >= 5:
        temp = main(Rarr[i],i,1)
        kBm += temp[1]
        size += 1
        
        Varr.append(temp[0])
        Rval.append(Rarr[i])
        
kBm = kBm/size
print('avg kBm = {0}'.format(kBm))


# # Square V's to plot linear relation
Varr2 = Varr
for i in range(len(Varr2)):
    Varr2[i] = Varr2[i]**2

# Plot V-R relationship
plt.figure()
plt.plot(Rval,Varr2,'.')

r = np.linspace(0,400000,10000)
v = (4*kB*T0*r*Df)
plt.plot(r,v)

plt.xlabel('Resistance [Ohm]')
plt.ylabel('Voltage Squared [V**2]')
plt.title('Voltage squared as a function of resistance\n')
plt.legend(['Experimental','Theoretical'])
plt.grid(True)



