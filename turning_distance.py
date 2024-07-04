from __future__ import division
from sympy import *

def turning_distance():
    i, n, k = symbols('i n k', integer=True)
    # TODO: add/remove the call to doit() and compare the results with what Dr. K gets
    # return 2*pi*sqrt(Rational(1,(n*k))*Sum((Rational(1,k)*floor(i/n)-Rational(1,n)*floor(i/k))**2-(Rational(1,n)-Rational(1,k))**2, (i, 0, k*n)))
    # return 2*pi*sqrt(1/(n*k)*Sum((1/k*floor(i/n)-1/n*floor(i/k))**2-(1/n-1/k)**2, (i, 0, k*n)))
    return Sum((1/k*floor(i/n)-1/n*floor(i/k))**2-(1/n-1/k)**2, (i, 0, k*n)).doit()

print(turning_distance())
