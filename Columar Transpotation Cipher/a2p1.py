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

def encryptMessage(key:int, message: str):
    # craete the 2d array for the encrypt
    cipherTable = [[' _ ' for i in range(len(message))] for j in range(key)]
    
    # initial the first direction of the cipher table
    row = 0
    column = 0
    
    for text in message:
        # check if go dwon to enter the message or not 
        if row == 0:
            goDown = True
        if row == (key - 1):
            goDown = False
        # enter the message into the cipher table    
        cipherTable[row][column] = text
        # move the column
        column += 1
        # move the row
        if goDown:
            row += 1
        else:
            row -= 1
    
    # get the encypered message from the 2d cipher table        
    cipherText = []
    for i in range(key):
        for j in range(len(message)):
            text = cipherTable[i][j]
            if text != ' _ ':
                cipherText.append(text)
                
    # print(cipherText)
    return ''.join(cipherText)
            
    
        

def decryptMessage(key:int, message: str):
    # craete the 2d array for the decrypt
    cipherTable = [[' _ ' for i in range(len(message))] for j in range(key)]  
    
   # print(message)
    
    # initial the first direction of the cipher table
    row = 0
    column = 0    
    
    for text in message:
        # check if go dwon to enter the message or not 
        if row == 0:
            goDown = True
        if row == key - 1:
            goDown = False
        # enter the ' __ ' marker into the cipher table    
        cipherTable[row][column] = ' __ '
        # move the column
        column += 1
        # move the row
        if goDown:
            row += 1
        else:
            row -= 1
    
    # replace the message to the marker row by row to the cipher table
    index = 0
    for i in range(key):
        for j in range(len(message)):
            if cipherTable[i][j] != ' _ ' and index < len(message):
                cipherTable[i][j] = message[index]
                index += 1
    # print(cipherTable)
    
    # read the cipher table by column to collect all the message to the plaintext
    plainText = []
    for i in range(len(message)):
        for j in range(key):
            text = cipherTable[j][i]
            if text != ' _ ':
                plainText.append(text)                
    # print(plainText)
    return ''.join(plainText)    
    

def test():
    assert decryptMessage(3, encryptMessage(3, "CIPHERS ARE FUN")) == "CIPHERS ARE FUN"

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
