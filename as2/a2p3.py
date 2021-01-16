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

def decryptMessage(key:list, message: str):
    # simulate the number of column in grid
    numOfColumn = len(message)//len(key)
    columnCheck = len(message)%len(key)
    if columnCheck != 0:
        numOfColumn += 1
        
    # simulate the number of row    
    numOfRow = len(key)
    
    # simulate the number of "shaded boxes"
    numOfShadedBox = (numOfColumn * numOfRow) - len(message)
    
    # add marker for the shaded box
    markers = numOfShadedBox
    max_ = max(key)
    positions = []
    while markers != 0:
        index = key.index(max_)
        positions.append(index)
        max_ -= 1
        markers -= 1    
    positions.sort()
    for pos in positions:
        pos = (pos+1)*numOfColumn - 1
        message = message[:pos] + "*" + message[pos:]
    # print(message)
    
    # build the grid and put message into the grid
    plainTable = ['']*numOfColumn
    column = 0
    row = 0
    for symbol in message:
        plainTable[column] += symbol
        column += 1
        if (column == numOfColumn):
            column = 0
            row += 1
    # print(plainTable)  
    
    # sort the plaintext table by row
    plaintext = ['']*numOfRow
    for i in range(numOfColumn):
        for j in range(numOfRow):
            plaintext[j] += plainTable[i][j]
    # print(plaintext)
    
    # build the normal traspotation encrypt message
    plainTableSorted = ['']*numOfRow
    index = 0
    for k in key:
        plainTableSorted[k-1] = plaintext[index]
        index += 1
    mess = ''.join(plainTableSorted)
    # print(mess)
    
    # decrypt and get the real plaintext
    plaintextSorted = ['']*numOfColumn
    column = 0
    row = 0
    for symbol in mess:
        plaintextSorted[column] += symbol
        column += 1
        if (column == numOfColumn):
            column = 0
            row += 1   
    # print(plaintextSorted)  
    text = ''.join(plaintextSorted)
    
    # removw the marker if needed
    if numOfShadedBox != 0:
        text = text[:-numOfShadedBox]
        
    
    return text

def test():
    assert decryptMessage([2,4,1,5,3], "IS HAUCREERNP F") == "CIPHERS ARE FUN"
    # decryptMessage([1,3,2], "ADGCFBE")
    # decryptMessage([2,4,6,8,10,1,3,5,7,9], "XOV EK HLYR NUCO HEEEWADCRETL CEEOACT KD")
    # decryptMessage([3, 1, 2],'CFADGBEH')
    # decryptMessage([1,3,4,2],'AEXCGDHBFY')
    # decryptMessage([1,5,4,3,2],"AFKPEJODINCHMBGL") 

from sys import flags

if __name__ == "__main__" and not flags.interactive:
    test()
