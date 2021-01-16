#!/usr/bin/env python3

#---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2020 <<Insert your name here>>
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
Enhanced substitution cipher solver.
"""

import re, simpleSubCipher, simpleSubHacker

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def hackSimpleSub(message):
    """
    Simple substitution cipher hacker.
    First runs the textbook program to get an initial, potentially incomplete decipherment.
    Then uses regular expressions and a dictionary to decipher additional letters.
    """
    letterMap = simpleSubHacker.hackSimpleSub(message)
    #print(letterMap)
    messages = message.split()
    first_pass = simpleSubHacker.decryptWithCipherletterMapping(message, letterMap)
    #print(first_pass)
    words = first_pass.split()
    #print(words)
    unchecked_word = {}
    for word in words:
        if "_" in word:
            # find the index for the word
            position = words.index(word)
            
            # set the regular expression
            match_pattern = generateRE(word, messages[position], letterMap)            
            
            # remove all characters not required.
            word = re.sub('[^A-Za-z0-9_]', '', word)
            cipherword = re.sub('[^A-Za-z0-9_]', '',  messages[position]).upper()
            
            # find the matched word by using match pattern
            matched_word = matchRE(match_pattern)
            
            # set a new dictionary to store all the words with '_'
            if word not in unchecked_word.keys():
                unchecked_word[word] = (cipherword, matched_word)
    
    # update the key table
    for k in unchecked_word.keys():
        if len(unchecked_word[k][1]) == 1:
            letterMap = updateLetterMap(unchecked_word[k][0], unchecked_word[k][1][0], letterMap, k)
            letterMap = simpleSubHacker.removeSolvedLettersFromMapping(letterMap)
    
    # see if the all keys in key table only match one 
    redo = False
    for item in letterMap.keys():
        if len(letterMap[item]) != 1:
            redo == True
            break
    
    if redo:
        hackSimpleSub2(message, letterMap)
    else:
        return simpleSubHacker.decryptWithCipherletterMapping(message, letterMap)
                
def hackSimpleSub2(message, letterMap):
    messages = message.split()
    first_pass = simpleSubHacker.decryptWithCipherletterMapping(message, letterMap)
    #print(first_pass)
    words = first_pass.split()
    #print(words)
    unchecked_word = {}
    for word in words:
        if "_" in word:
            # find the index for the word
            position = words.index(word)
            
            # set the regular expression
            match_pattern = generateRE(word, messages[position], letterMap)            
            
            # remove all characters not required.
            word = re.sub('[^A-Za-z0-9_]', '', word)
            cipherword = re.sub('[^A-Za-z0-9_]', '',  messages[position]).upper()
            
            # find the matched word by using match pattern
            matched_word = matchRE(match_pattern)
            
            # set a new dictionary to store all the words with '_'
            if word not in unchecked_word.keys():
                unchecked_word[word] = (cipherword, matched_word)
    
    # update the key table
    for k in unchecked_word.keys():
        if len(unchecked_word[k][1]) == 1:
            letterMap = updateLetterMap(unchecked_word[k][0], unchecked_word[k][1][0], letterMap, k)
            letterMap = simpleSubHacker.removeSolvedLettersFromMapping(letterMap)
    
    # see if the all keys in key table only match one 
    redo = False
    for item in letterMap.keys():
        if len(letterMap[item]) != 1:
            redo == True
            break
    
    if redo:
        hackSimpleSub2(message, letterMap)
    else:
        return simpleSubHacker.decryptWithCipherletterMapping(message, letterMap)    

def updateLetterMap(cpword, plword, letterMap, dic_key):
    for i in range(len(dic_key)):
        if dic_key[i] == "_":
            letterMap[cpword[i]] = [plword[i]]
            
    return letterMap
        
        
def matchRE(regular_expression):
    matchedList = []
    file = open("dictionary.txt", "r")
    wordsRange = file.read().splitlines()
    file.close()
    for word in wordsRange:
        if re.match(regular_expression, word):
            matchedList.append(word)
    return matchedList
    
def generateRE(checkWord, regularWord, letterMap):
    reg_exp = ''
    checkWord = re.sub('[^A-Za-z0-9_]', '', checkWord)
    regularWord = re.sub('[^A-Za-z0-9_]', '', regularWord)
    for i in range(len(checkWord)):
        if (checkWord[i] != '_'):
            reg_exp += checkWord[i].upper()
        else:
            reg_exp += '[' + "".join(letterMap[regularWord[i].upper()]) + ']'
    

    return ("^"+reg_exp+"$")

            
def test():
    # Provided test.
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
    print(hackSimpleSub(message))
    # End of provided test.
    

if __name__ == '__main__':
    test()

