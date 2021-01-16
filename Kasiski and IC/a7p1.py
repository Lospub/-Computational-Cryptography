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
Assignment 7 Problem 1
"""

from sys import flags
import re, random
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def antiKasiski(key: str, plaintext: str):
    """
    Thwart Kasiski examination 
    """
    ciphertext = translateMessage(plaintext, key)
    repeatDict = findRepeatSequencesSpacings(ciphertext, key)
    
    # cipher the text and add dash until no repeated sequence in the ciphertext
    while (len(repeatDict) != 0):
        # add dash
        plaintextSet = modifieddashtext(ciphertext, repeatDict, plaintext)
        plaintext = plaintextSet[0]
        i_index = plaintextSet[1]
        ciphertext = translateMessage(plaintext, key) 
        # find repeated sequence for the rest part
        repeatDict = findRepeatSequencesSpacings(ciphertext[i_index:], key)
    #print(plaintext)
    
    #replace the dashs and get the modified text
    for i in range(len(plaintext)):
        if plaintext[i] == '-':
            plaintext = plaintext[0:i]+ random.choice(LETTERS) + plaintext[i+1:]
            
    # recheck
    if len(findRepeatSequencesSpacings(translateMessage(plaintext, key), key)) != 0:
        ciphertext = translateMessage(plaintext, key)
        repeatDict = findRepeatSequencesSpacings(ciphertext, key)
        
        # cipher the text and add dash until no repeated sequence in the ciphertext
        while (len(repeatDict) != 0):
            # add dash
            plaintextSet = modifieddashtext(ciphertext, repeatDict, plaintext)
            plaintext = plaintextSet[0]
            i_index = plaintextSet[1]
            ciphertext = translateMessage(plaintext, key) 
            # find repeated sequence for the rest part
            repeatDict = findRepeatSequencesSpacings(ciphertext[i_index:], key)
        #print(plaintext)
        
        #replace the dashs and get the modified text
        for i in range(len(plaintext)):
            if plaintext[i] == '-':
                plaintext = plaintext[0:i]+ random.choice(LETTERS) + plaintext[i+1:]
            
    return plaintext

def modifieddashtext(ciphertext, repeatDict, plaintext):
    # find the first repeated sequence 
    if (len(list(repeatDict.keys())) != 0):
        firstrepeated = list(repeatDict.keys())[0]
    else:
        return plaintext
    n = len(firstrepeated)
    
    # add dash sfter the first repeated sequence.
    newplaintext = ''
    for i in range(len(ciphertext)):
        key = ''
        if len(ciphertext) - i >= n:
            key = ciphertext[i:n+i]
        if key == firstrepeated:
            newplaintext = plaintext[0:n+i] + '-' + plaintext[n+i:]
            break
    
    i_index = n+i+1 
                
    return newplaintext, i_index
                       
   
def findRepeatSequencesSpacings(message, key):
    # Goes through the message and finds any 3 to key length letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message:
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message:
    seqSpacings = {} # Keys are sequences, values are lists of int spacings.
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq:
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message:
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # Initialize a blank list.

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence:
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings   
 
def translateMessage(message, key):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS.
            num += LETTERS.find(key[keyIndex]) # Add if encrypting.

            num %= len(LETTERS) # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            translated.append(LETTERS[num])

            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)
            
            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0            

    return ''.join(translated)


def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    print(antiKasiski("WICK","THOSEPOLICEOFFICERSOFFEREDHERARIDEHOMETHEYTELLTHEMAJOKETHOSEBARBERSLENTHERALOTOFMONEY"))
    print(antiKasiski("AAAAAB","AAAAABBBAAAA"))
    #print(antiKasiski("WICK","THOSEPOLICEOFFFICERSWOFFEREDHERARIDEHOMETHEDYTELLTHEZMAJOKETHOSEBARBERSLENTHERALOTOFMONEY"))
    #print(findRepeatSequencesSpacings("THOSEPOLICEOFF-ICERSOFFEREDHERARIDEHOMETHEYTELLTHEMAJOKETHOSEBARBERSLENTHERALOTOFMONEY","WICK"))
    #print(translateMessage("THOSEPOLICEOFFICERSOFFEREDHERARIDEHOMETHEYTELLTHEMAJOKETHOSEBARBERSLENTHERALOTOFMONEY","WICK"))
    #print(translateMessage("THOSEPOLICEOFFICERS-OFFEREDHERARIDEHOMETHEYTELLTHEMAJOKETHOSEBARBERSLENTHERALOTOFMONEY","WICK"))

# Invoke test() if called via `python3 a5p1.py`
# but not if `python3 -i a5p1.py` or `from a5p1 import *`
if __name__ == '__main__' and not flags.interactive:
    test()
