from __future__ import division
from sympy import *

def turning_distance(n, k):
    i = symbols('i', integer=True)
    # TODO: add/remove the call to doit() and compare the results with what Dr. K gets
    return 2*pi*sqrt(Rational(1,(n*k))*Sum((Rational(1,k)*floor(i/n)-Rational(1,n)*floor(i/k))**2-(Rational(1,n)-Rational(1,k))**2, (i, 0, k*n)))

print(turning_distance(3, 2))
