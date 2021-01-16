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
Assignment 8 Problems 1, 2 and 3
"""
from sys import flags
import re
import itertools
import modifieda6p1 as ng
import modifieda6p2 as ks

# English letter frequencies for calculating IMC
ENG_LETT_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
NONLETTERS_PATTERN = re.compile('[^A-Z]')
LETTER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def stringIMC(message):
    # create dictinary to store the occurs of each character
    letterDict = {}
    for i in message:
        keys = letterDict.keys()
        if i in keys:
            letterDict[i] += 1
        else:
            letterDict[i] = 1
            
    # calculate sum of ti*ei
    IMC = 0
    length = len(message)
    for i in letterDict.keys():
        IMC += (letterDict[i]/length)*(ENG_LETT_FREQ[i])    
    return IMC

def subIMC(message, keylen):
    # find the IMC list
    IMCList = []
    for i in range(keylen):
        # find sub squence
        subsequence = getNthSubkeysLetters(i+1, keylen, message)
        # find poossible sub squence decipherment
        possibleSubsq = getPossibleSubsequences(subsequence)
        # find IMC based on poossible sub squence decipherment
        IMC = getIMC(possibleSubsq)
        # build IMC list
        IMCList.append(IMC)
    return IMCList

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
    
def getPossibleSubsequences(squence):
    # decipher sub sequence
    sqList = []
    for i in range(len(LETTER)):
        newsquence = ''
        for c in squence:
            c_index = LETTER.find(c)
            newsquence += LETTER[(c_index - i) % 26]
        sqList.append(newsquence)
    return sqList
    
def getIMC(possibleSubsq):
    # build IMC dictionary
    IMC = {}
    for i in range(len(LETTER)):
        IMC[LETTER[i]] =  stringIMC(possibleSubsq[i])
    # sort dictionary by value and store in a list
    sorted_IMC = sorted(IMC.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_IMC
    
def vigenereKeySolver(ciphertext: str, keylength: int):
    """
    return a list of the ten most likely keys
    """
    ciphertext = ciphertext.upper()
    # get IMC lsit
    IMCList = subIMC(ciphertext, keylength)
    # get top ten possible keys
    keys = getPossibleKey(IMCList, keylength)
    return keys

        
def getPossibleKey(IMCList, keylength):
    # build the possible position
    sortList = list(itertools.product(range(6), repeat=keylength))
    # build the posible keyword dictionary
    keyDict = {}
    j = 0
    for i in range(len(sortList)):
        key = ''
        count = 0
        for k in sortList[i]:
            key += IMCList[j][k][0]
            count += IMCList[j][k][1]
            j += 1
            j = j % keylength       
        keyDict[key] = count
    # sort the key by total IMC
    sorted_key = sorted(keyDict.items(), key=lambda kv: kv[1], reverse=True)
    # select the top 10 
    keyList = []
    countt = 0
    for i in sorted_key:
        if countt < 10:
            keyList.append(i[0])
            countt += 1
        else:
            break
    return keyList
   
# code from assignment7 
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

# code from assignment7 
def subseqIC(ciphertext: str, keylen: int):
    """
    Return the average IC of ciphertext for 
    subsequences induced by a given a key length
    """
    suIMC = 0
    for i in range(keylen):
        # find subsequences
        subsequences = getNthSubkeysLetters(i+1, keylen, ciphertext)
        # calculate stringIC
        StringIC = stringIC(subsequences)
        # calculate sum
        suIMC += StringIC
    # calculate average    
    avarageIC = suIMC/keylen
    return avarageIC

# code from assignment7 
def keyLengthIC(ciphertext: str):
    """
    Return the top n keylengths ordered by likelihood of correctness
    Assumes keylength <= 10
    """
    # store each average IC to the IClist and build the Dictionary to store the keylength and the its average IC
    IClist = []
    PositionDict = {}
    for i in range(1,11):
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
    for i in range(2):
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

def hackVigenere(ciphertext: str):
    """
    return a string containing the key to the cipher
    """
    ciphertext = ciphertext.upper()
    # find possible keylength list
    keylengthlist = keyLengthIC(ciphertext)
    # build possible key dictionary
    possibleKeyList = {}
    # find the frequencies
    frequencies = ng.ngramsFreqsFromFile("wells.txt", 2)

    for i in keylengthlist:
        # find possible keyword lists
        keywords = vigenereKeySolver(ciphertext, i)
        #print(keywords)
        highest = 0
        key = keywords[0]
        # find the possible keyword with higest score based on key length
        for keyword in keywords:
            score = ks.keyScore(keyword, ciphertext, frequencies, 2)
            if score > highest:
                highest = score
                key = keyword
        possibleKeyList[key] = highest
    #print(possibleKeyList.keys())
    #print(possibleKeyList.values())
    
    # find the final solution for the key
    compare = 0
    finalword = ''
    for key in possibleKeyList.keys():
        if possibleKeyList[key] > compare:
            compare = possibleKeyList[key]
            finalword = key
    return finalword
            
def crackPassword():
    """
    hack password_protected.txt and print out the decrypted plaintext
    """
    file = open('password_protected.txt')
    ciphertext = file.read()
    file.close()
    key = hackVigenere(ciphertext)
    decryptedText = ks.translateMessage(key, ciphertext)
    print(decryptedText)  

def test():
    import time
    time_start = time.time()    
    crackPassword()
    time_end = time.time()
    print('Time function:', (time_end - time_start))
    
    # vigenereKeySolver Tests
    ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
    best_keys = vigenereKeySolver(ciphertext, 5)
    assert best_keys[0] == "EVERY"
    print(best_keys)

    ciphertext = "Vyc fnweb zghkp wmm ciogq dost kft 13 eobp bdzg uf uwxb jv dxgoncw rtag ymbx vg ucrbrgu rwth gemjzv yrq tgcwxf"
    best_keys = vigenereKeySolver(ciphertext, 6)
    assert best_keys[0] == "CRYPTO"
    print(best_keys)
    
    # hackVigenere Tests
    ciphertext = "XUOD QK H WRTEMFJI JOEP EBPGOATW JSZSZV OVVQY JWMY JHTNBAVR GU OMLLGG KYODPWU YSWMSH OK ZSSF AVZS BZPW"
    key = hackVigenere(ciphertext)
    #print(key)
    assert key == "ECGLISH"
    print(key)
    
    ciphertext = "A'q nrxx xst nskc epu qr uet zw ggx yfvdari, js B figu xh xmpu wheiqei mg xcbi fw xq nskc. Hkeslsytj fxueov iqlmptx t nitp phfk vzqx skq. Z gtf xgcp bl mu ymf tc vyi psc jv wiwemj Lx uswch ggx ucixh fgtenki qw xaw rqzwx gyvjmww lkj abfhqn."
    key = hackVigenere(ciphertext)
    assert key == "SECRET"
    print(key)
    
    ciphertext = "JDMJBQQHSEZNYAGVHDUJKCBQXPIOMUYPLEHQFWGVLRXWXZTKHWRUHKBUXPIGDCKFHBZKFZYWEQAVKCQXPVMMIKPMXRXEWFGCJDIIXQJKJKAGIPIOMRXWXZTKJUTZGEYOKFBLWPSSXLEJWVGQUOSUHLEPFFMFUNVVTBYJKZMUXARNBJBUSLZCJXETDFEIIJTGTPLVFMJDIIPFUJWTAMEHWKTPJOEXTGDSMCEUUOXZEJXWZVXLEQKYMGCAXFPYJYLKACIPEILKOLIKWMWXSLZFJWRVPRUHIMBQYKRUNPYJKTAPYOXDTQ"
    key = hackVigenere(ciphertext)
    assert key == "QWERTY"
    print(key)
    
if __name__ == '__main__' and not flags.interactive:
    test()
#ciphertext = "XUOD QK H WRTEMFJI JOEP EBPGOATW JSZSZV OVVQY JWMY JHTNBAVR GU OMLLGG KYODPWU YSWMSH OK ZSSF AVZS BZPW"
#key = vigenereKeySolver(ciphertext, 7)
#print(key)

#ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
#best_keys = vigenereKeySolver(ciphertext, 5)
#print(best_keys)