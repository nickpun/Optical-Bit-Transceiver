# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:45:08 2019

@author: Nick
"""

import numpy as np
import matplotlib.pyplot as plt

# define constants
Q = 1e-6
m = 0.1
t0 = 0
R = 1
tf = 1000
x0a = 1
x0b = 10
eps = 8.854e-12
k = 1/(4*np.pi*eps)
dt = 1
x0 = x0b

# set up arrays for position and time
tarr = np.linspace(t0,tf,tf+1)
xarr = []
varr = []

# define a function that returns the force or acceleration
def acc(t):
    return (-Q*Q*k*xarr[t]/(R**2+xarr[t]**2)**(3/2))/m

# set initial position and velocity
xarr = np.append(xarr,[x0],axis=0)
varr = np.append(varr,[0],axis=0)

# integrate equation of motion
vdt = 0
for i in range(1000):
    vdt = varr[i] + acc(i)*dt/2
    xarr = np.append(xarr,[xarr[i] + vdt*dt],axis=0)
    varr = np.append(varr,[vdt + acc(i+1)*dt/2],axis=0)

# plot trajectories
plt.figure()
plt.title('charge trajectory with initial condition x0 = 10 m')
plt.xlabel('Time [s]')
plt.ylabel('x-position [m]')
plt.plot(tarr,xarr)

plt.figure()
plt.title('charge velocity with initial condition x0 = 10 m')
plt.xlabel('Time [s]')
plt.ylabel('x-velocity [m/s]')
plt.plot(tarr,varr)
