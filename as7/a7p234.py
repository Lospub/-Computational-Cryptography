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
Assignment 7 Problems 2, 3, and 4
"""

from sys import flags
import re

NONLETTERS_PATTERN = re.compile('[^A-Z]')

def stringIC(text: str):
    """
    Compute the index of coincidence (IC) for text
    """
    # create dictinary to store the occurs of each character
    letterDict = {}
    for i in text:
        keys = letterDict.keys()
        if i in keys:
            letterDict[i] += 1
        else:
            letterDict[i] = 1
            
    # calculate sum of ci(ci-1)
    sumString = 0
    for o in letterDict.keys():
        sumString += letterDict[o]*(letterDict[o]-1)
        
    stringIC = sumString/(len(text)*(len(text)-1))
    return stringIC


def subseqIC(ciphertext: str, keylen: int):
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """
    sumIC = 0
    for i in range(keylen):
        # find subsequences
        subsequences = getNthSubkeysLetters(i+1, keylen, ciphertext)
        # calculate stringIC
        StringIC = stringIC(subsequences)
        # calculate sum
        sumIC += StringIC
    # calculate average    
    avarageIC = sumIC/keylen
    return avarageIC


def getNthSubkeysLetters(nth, keyLength, message):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    message = NONLETTERS_PATTERN.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)

def keyLengthIC(ciphertext: str, n: int):
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 20
    """
    # store each average IC to the IClist and build the Dictionary to store the keylength and the its average IC
    IClist = []
    PositionDict = {}
    for i in range(1,21):
        SubIC = subseqIC(ciphertext, i)
        IClist.append(SubIC)
        if SubIC not in PositionDict:
            PositionDict[SubIC] = [i]
        else:
            priv = PositionDict[SubIC]
            priv.insert(0,i)
            PositionDict[SubIC] = priv
    #print(PositionDict)
    
    # find top n keylengths ordered by likelihood of correctness
    IClist.sort(reverse=True)
    topIC = []
    for i in range(n):
        if len(PositionDict[IClist[i]]) == 1:
            topIC.append(PositionDict[IClist[i]][0])
        else:
            for k in range(len(PositionDict[IClist[i]])):
                topIC.append(PositionDict[IClist[i]][k])
    
    ICtop = [] 
    for i in topIC: 
        if i not in ICtop: 
            ICtop.append(i)
            
    return ICtop

def test():
    "Run tests"
    assert stringIC("ABA") == 1 / 3
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    print(subseqIC('PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA', 3))
    print(keyLengthIC("PPQCAXQVEKGYBNKMAZUHKNHONMFRAZCBELGRKUGDDMA", 5))
    assert keyLengthIC('VTTKNKOZVKQICZHZVJGIUAKYKVTTFTBKSIZVTTMXCDTMHOQIYLVOPMXURDLTUEXAGOQCNLGHTHITABVEGYUINT', 8) == [14, 16, 5, 9, 10, 15, 8, 7]
    assert keyLengthIC('MLWJNMUDUVGPGJGQCYEILSNXKXZXEERRWSYMAIKXTVWLHQWMXWLVTWWLYSJTLWAZGQWGMWWOXRHKHQTEXQXHNV', 8) == [17, 19, 10, 12, 4, 16, 2, 5]
    assert keyLengthIC('DLCAYGMOZBSUXJMHNSWTQYZCBXFOPYJCBYKRRIQOEPOWMWIROWRMEQOWDYVYCWGQRKORRCITORNBSKLPCWJMEV', 8) == [12, 6, 3, 15, 19, 9, 4, 13]
    assert keyLengthIC('OPKUHMTODMWCRSSONWHXYSIIIXJZTGDLHFKVCMYINVVWQHMZIFXTEUZALSEEJWKBVSIAXJIXZVVVBQSPGHNUYE', 8) == [11, 16, 9, 13, 18, 7, 3, 8]


# Invoke test() if called via `python3 a5p1.py`
# but not if `python3 -i a5p1.py` or `from a5p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
