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
Problem 2
"""

from sys import flags
import util
import os.path
import simpleSubHacker

LETTER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def evalDecipherment(text1: str, text2: str) -> [float, float]:
    """
    docstring
    """
    # read file if the enteried str are the file name 
    if os.path.exists(text1):
        fileObj1 = open(text1, 'r')
        ftext1 = fileObj1.read()[:-1]
        
    else:
        ftext1 = text1
        
    if os.path.exists(text2):
        fileObj2 = open(text2, 'r')
        ftext2 = fileObj2.read()[:-1]
        
    else:
        ftext2 = text2
    
    # case-insencitive    
    plaintext = ftext1.upper()
    versiontext = ftext2.upper()
    
    # remove the non-alphabet character    
    newplaintext = ''
    for t in plaintext:
        if t in LETTER:
            newplaintext += t
    
    #newversiontext1 = simpleSubHacker.decryptWithCipherletterMapping(versiontext, simpleSubHacker.hackSimpleSub(versiontext))
    # remove the non-alphabet character
    newversiontext = ''
    for t in versiontext:
        if t in LETTER:
            newversiontext += t
    
    
    #print(newversiontext)
            
    keyAccuray = findKeyAccuray(newplaintext, newversiontext)
    deciphermentAccuray = findDeciphermentAccuray(newplaintext, newversiontext)
    
    return [keyAccuray, deciphermentAccuray]


def findKeyAccuray(newplaintext, newversiontext):
    plaintextlist = list(newplaintext)
    #first100 = []
    #for i in range(len(plaintextlist)):
        #if i < len(versiontext):
            #first100.append(plaintextlist[i])
    #plaintextlist = first100
    
    # find unique
    uniqueplaintext = []
    for letter in plaintextlist:
        if letter not in uniqueplaintext:
            uniqueplaintext.append(letter)
    versiontextlist = list(newversiontext)
    uniqueversion = []
    for letter in versiontextlist:
        if letter not in uniqueversion:
            uniqueversion.append(letter)
    
    corrextKey = 0
    #print(len(plaintextlist))
    #print(len(versiontextlist))
    #print(len(uniqueplaintext))
    #print(len(uniqueversion))    
    for i in range(len(uniqueversion)):
        if uniqueplaintext[i] == uniqueversion[i]:
            corrextKey += 1
    keyAccuray = corrextKey/len(uniqueplaintext)
    return keyAccuray
    
    
    
def findDeciphermentAccuray(newplaintext, newversiontext):
    #print(plaintext)
    #print(versiontext)    
    #first100 = ''
    #for i in range(len(plaintext)):
        #if i < len(versiontext):
            #first100 += plaintext[i]
    #plaintext = first100
    #print(len(plaintext))
    #print(len(versiontext))
    correctDeci = 0
    for i in range(len(newplaintext)):
        if newplaintext[i] == newversiontext[i]:
            correctDeci += 1
            
    DeciLength = len(newplaintext)
            
    deciphermentAccuray = correctDeci/DeciLength
    return deciphermentAccuray

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    print(evalDecipherment("OD CHR H LSOAND WBUT THE OF HISOUT", "IT WAS A BRIGHT COLD DAY IN APRIL"))
    
    
if __name__ == '__main__' and not flags.interactive:
    test()
