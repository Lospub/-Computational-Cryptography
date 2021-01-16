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
Nomenclator cipher
"""
import random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def translateMessage(key, codebook, message, mode):
    """
    Encrypt or decrypt using a nomenclator.
    Takes a substitution cipher key, a message (plaintext or ciphertext),
    a codebook dictionary, and a mode string ('encrypt' or 'decrypt')
    specifying the action to be taken. Returns a string containing the
    ciphertext (if encrypting) or plaintext (if decrypting).
    """
    
    translate = ''
    if mode == "encrypt" :
        words = message.split()
        
        # set the value for codebook variable
        for i in range(len(words)):
            for keys in codebook:
                if words[i].upper() == keys.upper():
                    words[i] = random.choice(codebook[keys])
        newMessage = ' '.join(words)
        
        # encrypt message
        translate = encrypt(key, newMessage)
                
    if mode == "decrypt" :
        # decrypt message
        translate = decrypt(key, message)
        words = translate.split()
        
        # set the codebook variable back to plaintext
        for i in range(len(words)):
            for keys in codebook:
                for j in codebook[keys]:
                    if words[i] == j:
                        words[i] = keys
        translate = ' '.join(words)         
        
                
    return translate

def encrypt(key, newMessage):
    translate = ''
    for symbol in newMessage:
        if symbol.upper() in LETTERS:
            num = LETTERS.find(symbol.upper())
            if symbol.upper() != symbol:
                translate += key[num].lower()
            else:
                translate += key[num]
        else:
            translate += symbol
    return translate

def decrypt(key, message):
    translate = ''
    for symbol in message:
        if symbol.upper() in LETTERS:
            num = key.find(symbol.upper())
            if symbol.upper() != symbol:
                translate += LETTERS[num].lower()
            else:                
                translate += LETTERS[num]
        else:
            translate += symbol
            
    return translate

def encryptMessage(key, codebook, message):
    return translateMessage(key, codebook, message, 'encrypt')


def decryptMessage(key, codebook, message):
    return translateMessage(key, codebook, message, 'decrypt')


def test():
    # Provided test.
    key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    #LE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    message = 'At the University of Alberta, examinations take place in December and April for the Fall and Winter terms.'
    codebook = {'university':['1', '2', '3'], 'examination':['4', '5'], 'examinations':['6', '7', '8'], 'WINTER':['9']}
    cipher = translateMessage(key, codebook, message, 'encrypt')
    print(cipher)
    print(translateMessage(key, codebook, cipher, 'decrypt'))
    # End of provided test.

if __name__ == '__main__':
    test()

