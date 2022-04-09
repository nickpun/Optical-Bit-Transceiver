# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 12:47:51 2019

@author: Nick
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#LIST OF ALL INPUTS
fname = 'lab5x4x4b.csv'
x_name = 'Voltage input'
x_units = 'Volts'
y_name = 'Voltage output'
y_units = 'Volts' 
guesses = (6.5, 0)

# Constants
kB = 1.38e-23
T0 = 293

# Variables
fmin = 100
fmax = 5000
Df = fmax-fmin

###############################################################################
# loads data, plots guessed curve
###############################################################################

# definition of the fit function
def fit_function(x, m, b):
    return  m*x+b
#load the file "fname", defined above
#data = np.loadtxt(fname, delimiter=',', comments='#')
Rarr = [1795,2702,3300,3900,6750,11990,14990,
        27040,30000,38780,38790,55800,120000,199400,270700,301800,392200]
Varr = [4.548104493636845e-07, 5.329464218237057e-07, 5.720912198018073e-07, 
        6.015782640238278e-07, 7.778575272208197e-07, 9.941049685339602e-07, 
        1.1088930478613116e-06, 1.4835034841573599e-06, 1.5769252859170299e-06, 
        1.749948385989782e-06, 1.7669469283526223e-06, 2.147409103128752e-06, 
        3.139431464956318e-06, 4.102918991906118e-06, 4.8533424513524925e-06, 
        5.146413831281512e-06, 5.9795741171838505e-06]
Uarr = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# access the data columns and assign variables x,y  and  y_sigma
x = Rarr
y = Varr
y_sigma = Uarr
y_sigma=5*y_sigma
# define an array of points  used or plotting the theory function
x_fitfunc=np.linspace(min(x),max(x),500)
    
#compares the guessed curve to the data for visual reference
y_guess = fit_function(x_fitfunc,*guesses)
plt.errorbar(x,y,yerr=y_sigma,marker='.',linestyle='',label="measured data")
plt.plot(x_fitfunc,y_guess,marker="",linestyle="-",linewidth=1,color="g",
         label="initial guess")
plt.xlabel('{} [{}]'.format(x_name,x_units))
plt.ylabel('{} [{}]'.format(y_name,y_units))
plt.title('Comparison between the data and the intial guess')
plt.legend(loc='best',numpoints=1)
print ('Displaying plot 1')
plt.show()

fit_params,fit_cov = curve_fit(fit_function,x,y,sigma=y_sigma,p0=guesses,
                               maxfev=10**5)
                               
###############################################################################
# prints the chi2 
###############################################################################

# function that  calculates the chi square value of a fit
def chi_square (fit_parameters, x, y, sigma):
#
    return np.sum((y-fit_function(x, *fit_parameters))**2/sigma**2)
    
# calculate and print chi square as well as the per degree-of-freedom value
chi2 = chi_square(fit_params,x,y,y_sigma)
dof = len(x) - len(fit_params)
print ("\nGoodness of fit - chi square measure:")
print ("Chi2 = {}, Chi2/dof = {}\n".format(chi2, chi2/dof))

###############################################################################
# prints the fit parameters (with uncertainty)
###############################################################################

fit_cov = fit_cov*dof/chi2
# calculate the standard deviation as uncertainty of the fit parameters
fit_params_error = np.sqrt(np.diag(fit_cov))

# read out parameter results
param_names = ['gain','y intercept']
print ("Fit parameters:")
for i in range(len(fit_params)):
    print ('{} = {:.3e} +/- {:.3e}'.format(param_names[i],
                                          fit_params[i],
                                          fit_params_error[i]))

                                                                        
###############################################################################
# plots the data and the fit curve
###############################################################################
    
y_fitfunc = fit_function(x_fitfunc,*fit_params)
plt.errorbar(x,y,yerr=y_sigma,marker='.',linestyle='',label="measured data")
plt.plot(x_fitfunc,y_fitfunc,marker="",linestyle="-",linewidth=2,color="r",
         label=" fit")
plt.xlabel('{} [{}]'.format(x_name,x_units))
plt.ylabel('{} [{}]'.format(y_name,y_units))
plt.legend(loc='best',numpoints=1)
print ('Displaying plot 2')
plt.show()


###############################################################################
# plots residual and histogram of residual. Don't touch this par tof the code
###############################################################################

# residual is the difference between the data and theory
y_fit=fit_function(x,*fit_params)
residual = y-y_fit
#calculate normalized residuals
normresidual=residual/y_sigma
# creates a histogram of the normalized residuals
hist,bins = np.histogram(normresidual,bins=30)

fig = plt.figure(figsize=(7,10))
ax1 = fig.add_subplot(211)
ax1.errorbar(x,residual,yerr=y_sigma,marker='.',linestyle='',
             label="residual (y-y_fit)")
ax1.hlines(0,np.min(x),np.max(x),lw=2,alpha=0.8)
ax1.set_xlabel('{} [{}]'.format(x_name,x_units))
ax1.set_ylabel('y-y_fit [{}]'.format(y_units))
ax1.legend(loc='best',numpoints=1)
ax2 = fig.add_subplot(212)
ax2.bar(bins[:-1],hist,width=bins[1]-bins[0])

ax2.set_ylim(0,1.2*np.max(hist))
ax2.set_xlabel('(y-y_fit)/y_sigma')
ax2.set_ylabel('Number of occurences')
plt.title('Histogram  of normalized residuals')
within_err=100.*np.sum((residual<=y_sigma)&(residual>=-y_sigma))/len(residual)
print ("\nResidual information:")
print ('{:.1f}% of data points agree with fit'.format(within_err))
ax2.vlines(-1.0,0,np.max(hist)*1.3,lw=3,color='r',linestyles='--')
ax2.vlines(+1.0,0,np.max(hist)*1.3,lw=3,color='r',linestyles='--',label='+/- error')
ax2.text(0.0,np.max(hist)*1.1,'{:.1f}% of data within one sigma of fit'.format(within_err),
         horizontalalignment='center',verticalalignment='center')
ax2.legend(loc=(0.35,0.05))

print ('\nDisplaying plot 3')
plt.show()