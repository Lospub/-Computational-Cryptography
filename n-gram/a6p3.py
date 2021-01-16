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
Problem 3
Version 1.2
"""

from sys import flags
import itertools
import a6p2

def bestSuccessor(mapping: dict, ciphertext: str, frequencies: dict, n: int) -> dict:
    # create the swaping list
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    switchList = list(itertools.combinations(SYMBOLS, 2))    
    
    # inisital current working successor apping
    currentSuccessor = mapping.copy()
    
    # inisital the best successor mapping
    bestSuccessor = mapping.copy()
    
    # inisital the higher score
    higherScore = a6p2.keyScore(mapping, ciphertext, frequencies, n)

    for i in switchList:
        
        # choosing two keys and exchange their value
        currentSuccessor[i[0]], currentSuccessor[i[1]] = currentSuccessor[i[1]], currentSuccessor[i[0]]
        
        # find the score of the current working successor mapping
        currentScore = a6p2.keyScore(currentSuccessor, ciphertext, frequencies, n)
        
        # find the higher score and the best successor mapping
        if (currentScore > higherScore):
            higherScore = currentScore
            bestSuccessor = currentSuccessor.copy()
        elif currentScore == higherScore:
            bestSuccessor = breakKeyScoreTie(mapping, bestSuccessor, currentSuccessor)
        
        # reset the current working successor mapping for next switch
        currentSuccessor = mapping.copy()

    return bestSuccessor


def breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB):
    """
    Break the tie between two successor mappings that have the same keyscore

    originalMapping: mapping the the other parameters are successors to
    successorMappingA: mapping that has had two keys swapped
    successorMappingB: mapping that has had two other keys swapped

    Example usage:
    originalMapping = {"A": "A", "B": "B", "C": "C"}
    # Mapping with B and C switched
    successorMappingA = {"A": "A", "B": "C", "C": "B"}
    # Mapping with A and C switched
    successorMappingB = {"A": "C", "B": "B", "C": "A"}

    # AC < BC so this function will return successorMappingB
    assert breakKeyScoreTie(originalMapping, successorMappingA, successorMappingB) == successorMappingB

    """
    aSwapped = "".join(sorted(k for k, v in (
        set(successorMappingA.items()) - set(originalMapping.items()))))
    bSwapped = "".join(sorted(k for k, v in (
        set(successorMappingB.items()) - set(originalMapping.items()))))
    return successorMappingA if aSwapped < bSwapped else successorMappingB


def test():
    "Run tests"
    # TODO: test thoroughly by writing your own regression tests
    # This function is ignored in our marking
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C"}, {"A": "A", "B": "C", "C": "B"}, {
                            "A": "C", "B": "B", "C": "A"}) == {"A": "C", "B": "B", "C": "A"}
    assert breakKeyScoreTie({"A": "A", "B": "B", "C": "C", "D": "D"}, {
                            "A": "B", "B": "A", "C": "C", "D": "D"}, {"A": "A", "B": "B", "C": "D", "D": "C"}) == {"A": "B", "B": "A", "C": "C", "D": "D"}


if __name__ == "__main__" and not flags.interactive:
    test()