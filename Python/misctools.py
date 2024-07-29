from __future__ import division
from math import *
from numpy import matrix

def poisson_solve(B):
    """Poisson solver."""
    assert B.shape[0]==B.shape[1]
    n=B.shape[0] # B is n by n matrix
    Q=matrix([[sin(j*k*pi/n)*sqrt(2/(n+1)) for k in xrange(n)] for j in xrange(n)])
    Bbar=Q*B*Q
    Ubar=matrix([[0.]*n]*n)
    for j in xrange(n):
        for k in xrange(n):
            Ubar[j,k]=Bbar[j,k]/(4-2*cos(j*pi/n)-cos(k*pi/n))
    U=Q*Ubar*Q
    return U

def differentiate(values):
    """Numerical differentiation."""
    return ([values[0]-values[1]]
          + [values[i+1]-values[i-1]/2 for i in xrange(1,len(values)-1)]
          + [values[len(values)-1]-values[len(values)-2]])

#~ def differentiate(values, times=1):
    #~ from numpy.fft import fft, ifft
    #~ """Numerical differentiation using FFT."""
    #~ return ifft([(1j*index)**times*value for index, value in enumerate(fft(values))])