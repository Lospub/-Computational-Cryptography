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
Assignment 10
"""
from sys import flags
import os
from collections import Counter

def cliSSD(ciphertext: str, files):
    ciphertext = ciphertext.upper()
    cipher = removeSpace(ciphertext)
    cipherList = findDictionary(cipher)
    samples = {}
    for file in files:
        sample = open(file, "rt", encoding="utf8").read()
        sample = sample.upper()
        sampletext = removeSpace(sample)
        sampleList = findDictionary(sampletext)
        samples[file] = sampleList
    SSD_dic = findSSDMapping(cipherList, samples)
    return SSD_dic
    
def removeSpace(text):
    sampletext = ''
    for ch in text:
        if ch != " " and ch != "\n":
            sampletext += ch
    return sampletext

def findDictionary(text):
    frequncy_map = {}
    textLength = len(text)
    for i in text:
        if i not in frequncy_map.keys():
            frequncy_map[i] = 1
        else:
            frequncy_map[i] += 1
    for key in frequncy_map.keys():
        frequncy_map[key] = frequncy_map[key]/textLength
    frequncy_List = sorted(frequncy_map.items(), key=lambda x: x[1], reverse=True)
    return frequncy_List

def findSSDMapping(cipherList, samples):
    diff = {}
    for sample in samples.keys():
        sum_sqrt_diff = findSumDiff(samples[sample], cipherList)
        diff[sample] = sum_sqrt_diff
    return diff
        
def findSumDiff(sample, cipherList):
    largerSize, smallSize, same = findLongerSize(sample, cipherList)
    sum_diff = 0
    if same:
        for i in range(len(largerSize)):
            diff = largerSize[i][1] - smallSize[i][1]
            square = diff**2
            sum_diff += square
    else:
        for i in range(len(smallSize)):
            diff = largerSize[i][1] - smallSize[i][1]
            square = diff**2
            sum_diff += square
        for k in range(len(smallSize), len(largerSize)):
            square = largerSize[k][1]**2
            sum_diff += square
    #sum_diff = float("{:.6f}".format(sum_diff))
    return sum_diff

def findLongerSize(sample, cipherList):
    s_length = len(sample)
    c_length = len(cipherList)
    if s_length > c_length:
        return sample, cipherList, False
    elif s_length < c_length:
        return cipherList, sample, False
    else:
        return sample, cipherList, True

def cliDPD(ciphertext: str, files):
    ciphertext = ciphertext.upper()
    cipherWordList = ciphertext.split()
    cipherPatternDic = findPatternDic(cipherWordList)
    samples = {}
    for file in files:
        sample = open(file, "rt", encoding="utf8").read()
        sample = sample.upper()
        sampleList = sample.split()
        samplePatternDic = findPatternDic(sampleList)
        samples[file] = samplePatternDic
    DPD_dic = findDPDMapping(cipherPatternDic, samples)  
    return DPD_dic

def findDPDMapping(cipherPatternDic, samples):
    diff = {}
    for sample in samples.keys():
        sum_sqrt_diff = findSumDiff_DPD(samples[sample], cipherPatternDic)
        diff[sample] = sum_sqrt_diff
    return diff    

def findSumDiff_DPD(sample, cipherDic):
    keyList = []
    for key in sample.keys():
        if key not in keyList:
            keyList.append(key)
    for key in cipherDic.keys():
        if key not in keyList:
            keyList.append(key)
    diff_sum = 0
    for key in keyList:
        if (key in sample.keys()) and (key in cipherDic.keys()):
            diff = sample[key] - cipherDic[key]
        elif (key in sample.keys()) and (key not in cipherDic.keys()):
            diff = sample[key]
        else:
            diff = cipherDic[key]
        square = diff ** 2
        diff_sum += square
    return diff_sum
    
def findPatternDic(wordList):
    word_dic = {}
    length = len(wordList)
    for word in wordList:
        wordPattern = findPattern(word)
        if wordPattern not in word_dic.keys():
            word_dic[wordPattern] = 1
        else:
            word_dic[wordPattern] += 1
    for k in word_dic.keys():
        word_dic[k] = word_dic[k] / length

    return word_dic

def findPattern(word):
    dic = Counter(word)
    pattern = tuple(sorted(tuple(dic.values())))
    return pattern


def countCorrectness(freqDic, lang):
    frequncy_List_sorted = sorted(freqDic.items(), key=lambda x: x[1])
    if frequncy_List_sorted[0][0] == "samples/sample_{a}.txt".format(a=lang):
        count = 1
    else:
        lang = frequncy_List_sorted[0][0]
        count = 0
    return count, lang


def test():
    
    lang_list = ["bg", "de", "el", "en", "es", "fr", "it", "nl", "pl", "ru"]
    count_ssd = 0
    ssd_lang_list = []
    count_dpd = 0
    dpd_lang_list = []
    for i in lang_list:
        print(i)
        for j in range(10):
            #print("ciphertexts/ciphertext_{a}_{b}.txt:".format(a=i, b=j))
            SSD = cliSSD(open("ciphertexts/ciphertext_{a}_{b}.txt".format(a=i, b=j), "rt", encoding="utf8").read(), ["samples/sample_bg.txt", "samples/sample_de.txt", "samples/sample_el.txt", "samples/sample_en.txt", "samples/sample_es.txt", "samples/sample_fr.txt", "samples/sample_it.txt", "samples/sample_nl.txt", "samples/sample_pl.txt", "samples/sample_ru.txt",])
            count, lang = countCorrectness(SSD, i)
            count_ssd += count
            ssd_lang_list.append(lang)
            #ptint(SSD)
            DPD = cliDPD(open("ciphertexts/ciphertext_{a}_{b}.txt".format(a=i, b=j), "rt", encoding="utf8").read(), ["samples/sample_bg.txt", "samples/sample_de.txt", "samples/sample_el.txt", "samples/sample_en.txt", "samples/sample_es.txt", "samples/sample_fr.txt", "samples/sample_it.txt", "samples/sample_nl.txt", "samples/sample_pl.txt", "samples/sample_ru.txt",])
            count_, lang_ = countCorrectness(DPD, i)
            count_dpd += count_
            dpd_lang_list.append(lang_)
        print("SSD correctness count: ", count_ssd)
        print("SSD_{a} langarage list: ".format(a=i), ssd_lang_list)
        print("DPD correctness count: ", count_dpd)
        print("DPD_{a} langarage list: ".format(a=i), dpd_lang_list)
        count_ssd = 0
        ssd_lang_list = []
        count_dpd = 0
        dpd_lang_list = []        
    '''
    for j in range(10):
        #print("ciphertexts/ciphertext_{a}_{b}.txt:".format(a=i, b=j))
        SSD = cliSSD(open("ciphertexts/ciphertext_pl_{b}.txt".format(b=j), "rt", encoding="utf8").read(), ["samples/sample_bg.txt", "samples/sample_de.txt", "samples/sample_el.txt", "samples/sample_en.txt", "samples/sample_es.txt", "samples/sample_fr.txt", "samples/sample_it.txt", "samples/sample_nl.txt", "samples/sample_pl.txt", "samples/sample_ru.txt",])  
        frequncy_List_sorted = sorted(SSD.items(), key=lambda x: x[1])
        print(frequncy_List_sorted)
    
    SSD = cliSSD(open("ciphertexts/ciphertext_pl_{b}.txt".format(b=9), "rt", encoding="utf8").read(), ["samples/sample_bg.txt", "samples/sample_de.txt", "samples/sample_el.txt", "samples/sample_en.txt", "samples/sample_es.txt", "samples/sample_fr.txt", "samples/sample_it.txt", "samples/sample_nl.txt", "samples/sample_pl.txt", "samples/sample_ru.txt",])  
    '''
    print(cliSSD(open("ciphertexts/ciphertext_en_1.txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt"]))
    print(cliSSD(open("ciphertexts/ciphertext_fr_1.txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt"]))
    print(cliDPD(open("ciphertexts/ciphertext_en_1.txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt"]))
    print(cliDPD(open("ciphertexts/ciphertext_fr_1.txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt"]))
if __name__ == "__main__" and not flags.interactive:
    test()

