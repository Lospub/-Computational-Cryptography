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


from sys import flags

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def keyScore( keyword: str, ciphertext: str, frequencies: dict, n: int ) -> float:
    deciphertext = translateMessage(keyword, ciphertext)
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
    
def translateMessage(key, message):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS.
            num -= LETTERS.find(key[keyIndex]) # Subtract if decrypting.

            num %= len(LETTERS) # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)

    return ''.join(translated)

def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    
if __name__ == "__main__" and not flags.interactive:
    test()

