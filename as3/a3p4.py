#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2020 <<Junyao Cui>>
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential 
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including 
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
#---------------------------------------------------------------

"""
Linear Congruential Hacker
"""

from sys import flags

def euclidean_gcd(a, m):
    # ax + my = g = gcd(a,m)
    # by using Euclidean algorithm
    # when a = 0: simply (ax + my = gcd(a, m)), holds when x = 0, y = 1, since gcd(0, m) = m
    # Otherwise,  (a mod m)x' + ay'= gcd(a,m)
    if a == 0:
        return (m, 0, 1)
    else:
        g, y, x = euclidean_gcd(m % a, a)
        return (g, x - (m // a) * y, y)
    

def modInv(a, m):
    # before doing the modular inverse, the gcd(a, m) should be 1 
    # check the gcd(a, m)
    g, x, y = euclidean_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def crack_lcg(m, r1, r2, r3):
    """
    Return the values a and b that would be used to LCG generate r1, r2, and r3
    r1 = (a * r0 + b) % m 
    r2 = (a * r1 + b) % m
    r3 = (a * r2 + b) % m
    ...
    returns [a, b] or [0, 0] if no solution 
    """
    # find the difference between two equations
    d1 = r2 - r3
    d2 = r1 - r2
    
    # positive all the elements
    if d1 < 0:
        d1 += m
    if d2 < 0:
        d2 += m
    
    # find the inverse of the modular
    inverse = modInv(d2, m)
    
    # check if the inverse exist, if not, return [0,0]
    if inverse == None:
        return ([0,0])
    
    # work out the actural a and b
    a = (inverse*d1) % m
    b = (r2 - (r1 * a)) % m
    
    return ([a, b])
    
def test():
    """
    Basic tests for crack_lcg
    """
    #print(crack_lcg(9, 4, 7, 4),
    #crack_lcg(3, 1, 1, 1),
    #crack_lcg(7, 4, 4, 4),
    #crack_lcg(10, 0, 4, 0),
    #crack_lcg(16, 0, 12, 0))    
    #euclidean_gcd(10,5)
if __name__ == "__main__" and not flags.interactive:
    test()
