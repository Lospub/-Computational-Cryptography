#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.1
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
Problem 1
"""

from sys import flags
import os



def ngramsFreqsFromFile(textFile, n) -> dict:
    # read file from path
    fileObj = open(textFile)
    ftext = fileObj.read().upper()
    fileObj.close()
    # remove unchecked character
    checkString = ''
    for text in ftext:
        if text.isascii():
            checkString += text
    
    #checkString = 'ABCDCD'
    # set frequency dictionary
    freqDictionary = {}
    keylist = []
    for i in range(len(checkString)):
        if len(checkString) - i >= n:
            key = ''
            for k in range(i,n+i):
                key += checkString[k]
            keylist.append(key)
    
    # count occurs
    for key in keylist:
        if key not in freqDictionary.keys():
            freqDictionary[key] = 1
        else:
            freqDictionary[key] += 1
    #print(freqDictionary['AB'])
    # colculate frequency
    for ke in freqDictionary.keys():
        freqDictionary[ke] = freqDictionary[ke] / len(keylist)
    
    return freqDictionary

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    print(ngramsFreqsFromFile("C:/Users/zhjyy/Desktop/1.txt", 2))
if __name__ == "__main__" and not flags.interactive:
    test()
