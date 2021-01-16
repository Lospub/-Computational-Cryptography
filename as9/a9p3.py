#!/usr/bin/env python3

# ---------------------------------------------------------------
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
# ---------------------------------------------------------------

"""
Assignment 9 Problem 3
"""

from sys import flags
from typing import List

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def blockSizeHack(blocks: List[int], n: int, e: int) -> str:
    """
    Hack RSA assuming a block size of 1
    """
    blockSize = 1
    messageLength = len(blocks)

    factors = getPrimeFactor(n)
    if len(factors) != 2:
        print("The number n should only have two prime factors.")
        exit()
    #print(factors)
    
    p = factors[0]
    q = factors[1]
    
    modul = (p - 1) * (q - 1)
    
    d = modInv(e, modul)
    
    key = (n, d)
    
    plaintext = decryptMessage(blocks, messageLength, key, blockSize)
    return plaintext
    
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

def getPrimeFactor(n):
    i = 2
    factors = []
    while i <= n:
        if (n % i) == 0:
            factors.append(i)
            n = n / i
        else:
            i = i + 1
    return factors

# codde from text book
def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)

def getTextFromBlocks(blockInts, messageLength, blockSize):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer:
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)

def test():
    "Run tests"
    blocks = [2361958428825, 564784031984, 693733403745, 693733403745,2246930915779, 1969885380643]
    n = 3328101456763
    e = 1827871
    assert blockSizeHack(blocks, n, e) == "Hello."
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

# Invoke test() if called via `python3 a5p1.py`
# but not if `python3 -i a5p1.py` or `from a5p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
