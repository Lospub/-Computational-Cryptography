#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2020 Xiyuan Shen
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
Assignment 10
"""
import string
import re

def cliSSD(ciphertext: str, files):
    cipherSSD = getSSD(ciphertext)
    lis = []
    for i in files:
        txt = open(i, "rt", encoding="utf8").read()
        lis.append(getSSD(txt))
    pos_record = {}
    for i in range(len(lis)):
        SSD = calcuSSD(cipherSSD,lis[i])
        # pos_record.append([i,SSD])
        pos_record[files[i]] = SSD
    # pos_record =  sorted(pos_record,key=getSecond,reverse=True)
    # return_dic = {}
    # for i in pos_record:
    #     return_dic[files[i[0]]] = i[1]
    print(pos_record)
    return pos_record

def calcuSSD(t1:list,t2:list):
    stand = 0
    diff = 0
    diff2 = 0
    if len(t1) >= len(t2):
        stand = len(t1)
        diff = len(t1)-len(t2)
    else:
        stand = len(t2)
        diff2 = len(t2)-len(t1)
    for count in range(diff):
        t2.append([0,0])
    for count in range(diff2):
        t1.append([0,0])
    SSD = 0
    for i in range(len(t1)):
        a = t1[i][1]
        b = t2[i][1]
        SSD += (a-b)**2
    return SSD

    
def getSSD(text:str):
    lis = []
    exclude = set(string.punctuation+"\n"+" ")
    text = ''.join(ch for ch in text if ch not in exclude).upper()
    for i in text:
        lis.append(i)
    counts = [[word, lis.count(word) / len(lis)] for word in set(lis)] 
    counts = sorted(counts,key=getSecond,reverse=True)
    return counts
    
def getSecond(lis):
    return lis[1]

#Part2

def cliDPD(ciphertext: str, files):
    cipherDPD = getDPD(ciphertext)
    lis = []
    for i in files:
        txt = open(i, "rt", encoding="utf8").read()
        lis.append(getDPD(txt))
    return_dic = {}
    for i in range(len(files)):
        return_dic[files[i]] = calcuSSD2(cipherDPD,lis[i])
    print(return_dic)
    return return_dic
    
def calcuSSD2(t1,t2):
    SSD2 = 0
    if (len(t1)>= len(t2)):
        temp = list(t1.keys())
        for i in temp:
            a = t1[i]
            b = 0
            if t2.get(i) is not None:
                b = t2[i]
            else:
                b = 0
            SSD2 += (a-b)**2
    else:
        temp = list(t2.keys())
        for i in temp:
            a = 0
            if t1.get(i) is not None:
                a = t1[i]
            else: 
                a = 0
            b = t2[i]
            SSD2 += (a-b)**2
    return SSD2

def getDPD(text:str):
    exclude = set(string.punctuation)
    
    split_word = text.upper().split()
    return_dic = {}
    lis = []
    for i in split_word:
        lis.append(getPattern(i))
    for i in lis:
        return_dic[str(i)] = lis.count(i)/len(split_word)
    return return_dic

def getPattern(word):
    lis = {}
    for i in word:
        lis[i] = 0
    for i in word:
        lis[i] += 1
    return_lis = sorted(lis.values(),reverse=True)
    return (return_lis)
 
def test():
    # cliSSD(open("ciphertext_en_1.txt", "rt", encoding="utf8").read(), ["sample_en.txt", "sample_fr.txt"])
    # cliSSD(open("ciphertext_fr_1.txt", "rt", encoding="utf8").read(), ["sample_en.txt", "sample_fr.txt"])
    print(cliDPD(open("ciphertexts/ciphertext_en_1.txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt"]))
    print(cliDPD(open("ciphertexts/ciphertext_fr_1.txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt"]))
# if __name__ == "__main__" and not flags.interactive:
test()

