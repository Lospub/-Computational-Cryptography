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
CMPUT 331 Assignment 1 Student Solution
September 2020
Author: <Junyao Cui>
"""
NUM_SYM = 52

def encrypt(message: str, key: str):
    # every possible symbol that can be encrypted
    LETTERS = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz' 
    
    # stores the encrypted/decrypted form of the message
    translated = ''
    
    #find the number of key
    key = LETTERS.find(key)
    
    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        if symbol in LETTERS:
            # get the encrypted (or decrypted) number for this symbol
            new_key = LETTERS.find(symbol) # get the number of the symbol
            num = new_key + key
            key = new_key
            # handle the wrap-around if num is larger than the length of
            # LETTERS or less than 0
            if num >= len(LETTERS):
                num = num - len(LETTERS)
            elif num < 0:
                num = num + len(LETTERS) 
            # add encrypted/decrypted number's symbol at the end of translated
            translated = translated + LETTERS[num]
        else:
            # just add the symbol without encrypting/decrypting
            translated = translated + symbol    
            
    return translated
    

def decrypt(message: str, key: int):
    # every possible symbol that can be encrypted
    LETTERS = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz' 
    
    # stores the encrypted/decrypted form of the message
    translated = ''
    
    #find the number of key
    #key = LETTERS.find(key)    
    
    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        if symbol in LETTERS:
            # get the encrypted (or decrypted) number for this symbol
            num = LETTERS.find(symbol) # get the number of the symbol
            num = num - key
            # handle the wrap-around if num is larger than the length of
            # LETTERS or less than 0
            if num >= len(LETTERS):
                num = num - len(LETTERS)
            elif num < 0:
                num = num + len(LETTERS) 
            # add encrypted/decrypted number's symbol at the end of translated
            translated = translated + LETTERS[num]
            key = num
        else:
            # just add the symbol without encrypting/decrypting
            translated = translated + symbol  
            
    return translated

def test():
    #assert decrypt(encrypt("!foo", "g"), "g") == "!foo"
    decrypt("!cVAP", "W")

from sys import flags
    
if __name__ == "__main__" and not flags.interactive:
    test()
