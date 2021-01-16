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

def keyScore( mapping: dict, ciphertext: str, frequencies: dict, n: int ) -> float:
    deciphertext = translateMessage(mapping, ciphertext)
    totalscore = 0.0
    
    # initial the ngram occurs count 
    occurs = {}
    for item in frequencies:
        occurs[item] = 0
    for i in range(len(deciphertext)):
        if len(deciphertext) - i >= n:
            key = deciphertext[i:n+i]
            if key in occurs.keys():
                occurs[key] += 1
    # calculate total score
    for key in frequencies.keys():
        count = occurs[key]
        frequency = frequencies[key]
        score = count * frequency
        totalscore += score
    #print(totalscore)
    return float(totalscore)
    
def translateMessage(mapping, message):
    translated = ''

    # Loop through each symbol in message:
    for symbol in message:
        if symbol in mapping.keys():
            translated += mapping[symbol]
        else:
            translated += symbol

    return translated

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    
if __name__ == "__main__" and not flags.interactive:
    test()





