from __future__ import division
from sympy import symbols, nsimplify, summation, floor

def turning_distance(n, k):
    i = symbols('i', integer=True)
    return nsimplify(4/(n*k)*summation((1/k*floor(i/n)-1/n*floor(i/k))**2, (i, 0, k*n-1))-(1/n-1/k)**2, rational=True)

print(turning_distance(5, 3))
