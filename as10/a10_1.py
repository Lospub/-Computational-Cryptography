#!/usr/bin/env python3

# ---------------------------------------------------------------
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
# ---------------------------------------------------------------

"""
Assignment 10
"""
from sys import flags
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
def cliSSD(ciphertext: str, files):
    ciphertext = ciphertext.lower()
    result = dict()
    cipher_SSD = dict()
    value_sum1 = 0
    for symbol in ciphertext.replace("\n", ""):
        if symbol not in cipher_SSD and not symbol.isspace():
            cipher_SSD[symbol] = 1
            value_sum1 += 1
        elif symbol in cipher_SSD and not symbol.isspace():
            cipher_SSD[symbol] += 1
            value_sum1 += 1
    for item in cipher_SSD:
        cipher_SSD[item] = cipher_SSD[item]/value_sum1  
    cipher_SSD = sorted(cipher_SSD.items(), key=lambda x:x[1], reverse=True)
    
    for file in files:
        sample = open(file, "rt", encoding="utf8").read().lower()
        sample_SSD = dict()
        value_sum2 = 0
        for symbol in sample.replace("\n", ""):
            if symbol not in sample_SSD and not symbol.isspace():
                sample_SSD[symbol] = 1
                value_sum2 += 1
            elif symbol in sample_SSD and not symbol.isspace():
                sample_SSD[symbol] += 1
                value_sum2 += 1
        for item in sample_SSD:
            sample_SSD[item] = sample_SSD[item]/value_sum2
        sample_SSD = sorted(sample_SSD.items(), key=lambda x:x[1], reverse=True)
        SSD = 0
        for i in range(max(len(cipher_SSD),len(sample_SSD))):
            if i < min(len(cipher_SSD),len(sample_SSD)):
                SSD += (cipher_SSD[i][1]-sample_SSD[i][1])**2
            elif len(cipher_SSD)>len(sample_SSD):
                SSD += (cipher_SSD[i][1])**2
            else:
                SSD += (sample_SSD[i][1])**2
        result[file] = SSD
    result = sorted(result.items(), key=lambda x:x[1])
    print(result)
    return result

def cliDPD(ciphertext: str, files):
    ciphertext = ciphertext.lower()
    cipher_DPD = dict()
    result = dict()
    value_sum1 = 0
    for word in ciphertext.split():
        distinct_letter = dict()
        for symbol in word:
            if symbol not in distinct_letter:
                distinct_letter[symbol] = 1
            else:
                distinct_letter[symbol] += 1
        distinct_letter = sorted(distinct_letter.items(), key=lambda x:x[1], reverse=True)
        key = ()
        for i in range(len(distinct_letter)):
            key += (distinct_letter[i][1],)
        if key not in cipher_DPD:
            cipher_DPD[key] = 1
            value_sum1 += 1
        else:
            cipher_DPD[key] +=1
            value_sum1 += 1
    for item in cipher_DPD:
        cipher_DPD[item] = cipher_DPD[item]/value_sum1

    for file in files:
        sample = open(file, "rt", encoding="utf8").read().lower()
        sample_DPD = dict()
        value_sum2 = 0
        for word in sample.split():
            distinct_letter = dict()
            for symbol in word:
                if symbol not in distinct_letter:
                    distinct_letter[symbol] = 1
                else:
                    distinct_letter[symbol] += 1
            distinct_letter = sorted(distinct_letter.items(), key=lambda x:x[1], reverse=True)
            key = ()
            for i in range(len(distinct_letter)):
                key += (distinct_letter[i][1],)
            if key not in sample_DPD:
                sample_DPD[key] = 1
                value_sum2 += 1
            else:
                sample_DPD[key] += 1
                value_sum2 += 1
        for item in sample_DPD:
            sample_DPD[item] = sample_DPD[item]/value_sum2

        DPD = 0
        for item in cipher_DPD:
            if item in sample_DPD:
                DPD += (cipher_DPD[item]-sample_DPD[item])**2
            else:
                DPD += (cipher_DPD[item])**2
        for item in sample_DPD:
            if item not in cipher_DPD:
                DPD += (sample_DPD[item])**2

        result[file] = DPD
    result = sorted(result.items(), key=lambda x:x[1])
    print(result)
    return result
  
  
def test():
    for i in range(10):
        cliSSD(open("ciphertexts/ciphertext_pl_"+str(i)+".txt", "rt", encoding="utf8").read(), ["samples/sample_en.txt", "samples/sample_fr.txt", "samples/sample_bg.txt", "samples/sample_de.txt", "samples/sample_el.txt", "samples/sample_es.txt", "samples/sample_it.txt", "samples/sample_nl.txt", "samples/sample_pl.txt", "samples/sample_ru.txt"])


if __name__ == "__main__" and not flags.interactive:
    test()

