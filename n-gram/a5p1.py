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
Subsititution cipher frequency analysis
"""

from sys import flags
from collections import Counter # Helpful class, see documentation or help(Counter)
import os

ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
LETTER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def freqDict(ciphertext: str) -> dict:
    """
    Analyze the frequency of the letters
    """
    if os.path.exists(ciphertext):
        fileObj = open(ciphertext, 'r')
        ftext = fileObj.read()[:-1]
        
    else:
        ftext = ciphertext      
    
    freqDictionary = {}
    cipherlist = list(ftext.upper())
    cipherlist.sort()
    listset = set(cipherlist)
    uniquelist = list(listset)
    #print(cipherlist)
    ciphertextCounter = Counter(cipherlist).most_common(len(uniquelist))
    #print(ciphertextCounter)
    
    for i in ciphertextCounter:
        if i[0] in LETTER:
            freqDictionary[i[0]] = i[1]
    for letter in LETTER:
        if letter not in freqDictionary.keys():
            freqDictionary[letter] = 0
    #print(freqDictionary)        
    
    for key in freqDictionary.keys():
        if freqDictionary[key] != 0:
            freqDictionary[key] = ETAOIN[list(freqDictionary).index(key)]
            
    #print(freqDictionary)
    return freqDictionary
    

def freqDecrypt(mapping: dict, ciphertext: str) -> str:
    """
    Apply the mapping to ciphertext
    """
    if os.path.exists(ciphertext):
        fileObj = open(ciphertext, 'r')
        ftext = fileObj.read()[:-1]
        
    else:
        ftext = ciphertext    
    plaintext = decryptWithCipherletterMapping(ftext, mapping)
    plaintext = plaintext.upper()
    return plaintext
     

def decryptWithCipherletterMapping(ciphertext, letterMapping):
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an _ underscore.

    # First create a simple sub key from the letterMapping mapping:
    key = ['x'] * len(LETTER)
    for cipherletter in LETTER:
        if letterMapping[cipherletter] != 0:
            # If there's only one letter, add it to the key.
            keyIndex = LETTER.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the ciphertext:
    return translateMessage(key, ciphertext, 'decrypt')


def translateMessage(key, message, mode):
    translated = ''
    charsA = LETTER
    charsB = key
    if mode == 'decrypt':
        # For decrypting, we can use the same code as encrypting. We
        # just need to swap where the key and LETTERS strings are used.
        charsA, charsB = charsB, charsA

    # Loop through each symbol in message:
    for symbol in message:
        if symbol.upper() in charsA:
            # Encrypt/decrypt the symbol:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # Symbol is not in LETTERS; just add it
            translated += symbol

    return translated


def test():
    "Run tests"
    #print(freqDict("HELLO WORLD"))
    #freqDecrypt(freqDict("HELLO WORLD"), "HELLO WORLD")
    print(freqDecrypt(freqDict("The quick brown fox jumps over the lazy dog"), "The quick brown fox jumps over the lazy dog"))
    print(freqDecrypt(freqDict("FEU GOXNH ZSMVK QMB WOJIP MYUS FEU CRAT LMD"), "FEU GOXNH ZSMVK QMB WOJIP MYUS FEU CRAT LMD"))
    assert type(freqDict("A")) is dict
    assert freqDict("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")["A"] == "E"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking

# Invoke test() if called via `python3 a5p1.py`
# but not if `python3 -i a5p1.py` or `from a5p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
