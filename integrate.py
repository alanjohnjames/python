###
### module integrate.py
###
import numpy as np
import scipy.integrate

def linear(x, m=1, c=0):
    return m*x + c
    
x = np.linspace(-1,1,5)
y = linear(x)

I = scipy.integrate.trapz(x,y)

def index(val, arr):
 return (np.abs(arr - val)).argmin()

print index(x, 0.75) 

x_int = []


