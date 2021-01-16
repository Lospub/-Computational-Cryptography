
import os, sys

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'



def freqDict(filename):
    inputFilename = filename
    outputFile_name = inputFilename + "_freqMapping" 
    fileObj = open(inputFilename)
    message = fileObj.read()
    
    
    cipherFreqOrder = getFrequencyOrder(message)
    # string 1 that got freq order in ciphertext
    plainFreqOrder = ETAOIN
    # string 2 that got freq order in plaintext
    freqMapping = dict.fromkeys(cipherFreqOrder)
    # freqMapping is the dictionary that contains keys-cFO and values-pFO
    i = 0
    for key in freqMapping:
        freqMapping[key] = plainFreqOrder[i]
        i += 1
    #return freqMapping
    outputFileObj_1 = open(outputFile_name, 'w')
    outputFileObj_1.write(str(freqMapping))
    outputFileObj_1.close()   
    return freqMapping
    
def freqDecrypt(inputFilename, outputFilename):
    freqMapping = freqDict(inputFilename)
    outputFile_name = outputFilename
    fileObj = open(inputFilename)
    message = fileObj.read()
    
    newMes = []    
    for letter in message:
        if LETTERS.find(letter) == -1:
            newMes.append(letter)
        else:
            for key in freqMapping:
                if letter == key:
                    newMes.append(freqMapping[key])                
    plaintext = "".join(newMes)
    #return plaintext
    outputFileObj_1 = open(outputFile_name, 'w')
    outputFileObj_1.write(str(plaintext))
    outputFileObj_1.close() 


def getLetterCount(message):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter.
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount
    
def getItemAtIndexZero(x):
    return x[0]

    
def getFrequencyOrder(message):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.

    # first, get a dictionary of each letter and its frequency count
    letterToFreq = getLetterCount(message)

    # second, make a dictionary of each frequency count to each letter(s)
    # with that frequency
    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    # third, put each list of letters in reverse "ETAOIN" order, and then
    # convert it to a string
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # fourth, convert the freqToLetter dictionary to a list of tuple
    # pairs (key, value), then sort them
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)

    # fifth, now that the letters are ordered by frequency, extract all
    # the letters for the final string
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)
    
    
def main():
    freqDict('text_1984_cipher')
    freqDecrypt('text_1984_cipher', '1984output')
    
main()
