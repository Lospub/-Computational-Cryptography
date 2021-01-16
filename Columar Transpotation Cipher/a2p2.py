#!/usr/bin/python3

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
CMPUT 331 Assignment 2 Student Solution
September 2020
Author: <Junyao Cui>
"""

def encryptMessage(key:list, message: str):
    cipherTable = ['']*len(key)
    
    # create the cipher table and put all the message into the table
    for column in range(len(key)):
        currentIndex = column
        while currentIndex < len(message):
            cipherTable[column] += message[currentIndex]
            currentIndex += len(key)
    
    # rebuild the order of items in cipher table by following the key in key list  
    # to get the excatly ciphertext
    ciphertext = ['']*len(key)
    index = 0
    for k in key:
        ciphertext[index] = cipherTable[k-1]
        if index < len(key):
            index += 1
    return ''.join(ciphertext)

def test():
    assert encryptMessage([2,4,1,5,3], "CIPHERS ARE FUN") == "IS HAUCREERNP F"

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
