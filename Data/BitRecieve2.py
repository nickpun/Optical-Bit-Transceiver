# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:01:50 2019

@author: Nick
"""

from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Parameters
# =============================================================================

# User Input Message
ans = [1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,
                         0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0]

# User Input Variables
wavFile = 'test25.wav'
lowFreq = 500       # [hertz]
numBitBins = 15
bitsPerBin = 8
tTime = 30         # [seconds]
separation = 5     # [hertz]

# User Calibration Variables
vThreshold = 2e-8  # [Volts]

# User Troubleshoot Controls
plotVversust = False
printVees = False
checkMatching = True
plotPxxDen = 0 #index of bin to plot (won't plot if given invalid bin index)

# System Scaling Factors
tScale = 8.055/355227
vScale = 1/300000
ampScale = 2200

# System Variables
freqs = []
bits = []

# =============================================================================
# Main
# =============================================================================

def main():
    # Get bits
    get_bits()
    
    # Check if bits matches answer (Troubleshoot)
    check_matching()
    
    # Print bits
    print('\nTranmitted bit message:')
    print(ans)
    print('\nRecieved bit message:')
    print(bits)

# =============================================================================
# Helper Functions
# =============================================================================

# Get all bits and put them into bits[]
def get_bits():
    # Create arrays
    a = read(wavFile)
    b = np.array(a[1],dtype=float)
    t = np.linspace(0, tTime, len(b))
    for i in range(2**bitsPerBin):
        freqs.append(lowFreq + i*separation)
    
    # Scale
    for i in range(len(b)):
        b[i,0] = b[i,0]*vScale
        #b[i,1] = b[i,1]*vscale # I don't actually use this
    
    # Get bits from each bit bin
    c = b[:,0]
    ptsPerBin = int(len(c)/numBitBins)
    for i in range(numBitBins):
        binResults = get_bin_bits(c[i*ptsPerBin : (i+1)*ptsPerBin-1], i)
        bits.extend(binResults)
    
    # Plot V vs t (Troubleshoot)
    plot_V_vs_t(t,b[:,0])

# Get the bits of a particular bin
def get_bin_bits(bitBin, binNum):
    # Initiate bin results array
    binResults = []
    
    # Generate power spectrum
    f, pxx_den = signal.periodogram(bitBin, 1/tScale)
    
    # Plot power spectrum (Troubleshoot)
    plot_pxx_den(f, pxx_den, binNum)
    
    # Get frequency sent
    ff = []
    for i in range(f):
        if f[i] >= lowFreq and f[i] < lowFreq*2:
            ff.append(f[i])
    fmax = ff[argmax(pxx_den[])]
    
    
    # Extract binary number into array
    binResults = [int(x) for x in bin(int(ind))[2:]]
    while len(binResults) < bitsPerBin:
        binResults = [0] + binResults
    print(binResults)
    
    # Return bin results
    return binResults

# =============================================================================
# Troubleshooting Functions
# =============================================================================

# Plot voltage on the time domain    
def plot_V_vs_t(t,V):
    if plotVversust == True:
        plt.figure()
        plt.get_current_fig_manager().window.showMaximized()
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [V]')
        plt.title('Voltage as a function of time')
        plt.xlim([0,2]) #comment out for graph of full data set
        plt.plot(t,V)

# Check if revieced bit message matches transmitted bit message
def check_matching():
    if checkMatching == True:
        print('\nChecking if recieved bit message matches transmitted bit '
              'message:')
        print('[index]-[bin number]-[index within bin]-[frequency]-'
              '{1=True, 0=False}')
        for i in range(len(ans)):
            if bits[i] == ans[i]:
                print('[{0}]-[{1}]-[{2}]-[{3}]-1'
                      .format(i, int(i/bitsPerBin), i%bitsPerBin, 
                              freqs[i%bitsPerBin]))
            else:
                print('[{0}]-[{1}]-[{2}]-[{3}]-0 '
                      '-> bits[{0}]={4} whereas ans[{0}]={5}'
                      .format(i, int(i/bitsPerBin), i%bitsPerBin, 
                              freqs[i%bitsPerBin], bits[i], ans[i]))
      
# Print voltage/integral of each bit
def print_Vees(V, binNum, fRangeNum):
    if printVees == True:
        i = binNum*bitsPerBin+fRangeNum
        if binNum==0 and fRangeNum ==0:
            print('\nVoltages of each frequency per bin:')
            print('[index]-[bin number]-[index within bin]-[frequency]-'
                  '[voltage reading]')
        print('[{0}]-[{1}]-[{2}]-[{3}]-[{4}]'
              .format(i, binNum, fRangeNum, freqs[fRangeNum], V))

# Plot the power spectrum of a particular bin
def plot_pxx_den(f, pxx_den, binNum):
    if plotPxxDen == binNum:
        plt.figure()
        plt.get_current_fig_manager().window.showMaximized()
        plt.xlabel('frequency [Hz]')
        plt.ylabel('PSD [V**2/Hz]')
        plt.title('Power Spectrum of bin {0}'.format(binNum))
        plt.xlim([lowFreq,2*lowFreq]) #comment out for graph of full data set
        #plt.ylim([10e-8,10e-2]) #comment out for graph of full data set
        plt.plot(f, pxx_den)
# =============================================================================
    
main()