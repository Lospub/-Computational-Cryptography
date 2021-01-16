# Simple Substitution Cipher Hacker
# https://www.nostarch.com/crackingcodes (BSD Licensed)

import re, copy, pyperclip, simpleSubCipher, wordPatterns, makeWordPatterns

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')




def secondPass(unSovledWords,letterMapping,ciphertext):
    # The 'unSovledWords' parameter is the unsovled words dictionary in the decrypted message and corresponding possible words in english dictionary
    # The `letterMapping` parameter is a "cipherletter mapping" dictionary
    # The `cipherword` parameter is a string value of the ciphertext.

    for k in unSovledWords.keys():
        if len(unSovledWords[k][0]) == 1:
            #To get characters corresponds unsovled words in ciphertext.
            cipherPattern = ciphertext[unSovledWords[k][1][0]:unSovledWords[k][1][1]]
            

            index = 0
            for i in cipherPattern:
                #Address one-to-one constraint.
                if  len(letterMapping[i.upper()])!= 1:
                    #To get the mapped character in possible words.
                    key = str(unSovledWords[k][0][0][index])
                    #Assign it to the letter mapping.
                    letterMapping[i.upper()] = [key]
                index+= 1
                
            # Remove any solved letters from the other lists:
            removeSolvedLettersFromMapping(letterMapping)
    return letterMapping
    


def findUnSovledWords(decryptMessage):
    #The `decryptMessage` parameter is a "decrpted message"
    #Return a dictionary encrpyted words and their possible english words from english dictionary and their position.
    unSovledWords = {}
    for word in decryptMessage.split():
        if '_' in word:
            #Remove all non-letters and digits characters.   
            word = re.sub('[^A-Za-z0-9\\_]+', '', str(word))

            #Get the start index and end index of encrypted word
            position = (decryptMessage.index(word), decryptMessage.index(word)+len(word))

            #Formming a regex.
            pattern = re.sub('_','[A-Za-z]',word)
            pattern = '^'+pattern+'$'

            #Get a dictionary unsovled words in this case key are encrpted words, 
            # values are possible english word from dictionary and its position in message.
            if word not in unSovledWords.keys():
                unSovledWords[word] = (checkWord(pattern),position)
    return unSovledWords

#From course material 
def checkWord(regex):
    resList = []
    wordFile = open('dictionary.txt') 
    for line in wordFile:
        if re.match(regex,line[:-1].lower()): 
            resList.append(line[:-1])
    return resList

def getBlankCipherletterMapping():
    # Returns a dictionary value that is a blank cipherletter mapping.
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    # The `letterMapping` parameter is a "cipherletter mapping" dictionary
    # value that the return value of this function starts as a copy of.
    # The `cipherword` parameter is a string value of the ciphertext word.
    # The `candidate` parameter is a possible English word that the
    # cipherword could decrypt to.

    # This function adds the letters of the candidate as potential
    # decryption letters for the cipherletters in the cipherletter
    # mapping.

    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])



def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and then add only the
    # potential decryption letters if they exist in BOTH maps.
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    # Cipherletters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other
    # letter. (This is why there is a loop that keeps reducing the map.)

    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # `solvedLetters` will be a list of uppercase letters that have one
        # and only one possible mapping in `letterMapping`:
        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # If a letter is solved, than it cannot possibly be a potential
        # decryption letter for a different ciphertext letter, so we
        # should remove it from those other lists:
        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again.
                        loopAgain = True
    return letterMapping


def hackSimpleSub(message):
    intersectedMap = getBlankCipherletterMapping()
    
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()
    
    for cipherword in cipherwordList:
        # Get a new cipherletter mapping for each ciphertext word:
        candidateMap = getBlankCipherletterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue # This word was not in our dictionary, so continue.

        # Add the letters of each candidate to the mapping:
        for candidate in wordPatterns.allPatterns[wordPattern]:
            addLettersToMapping(candidateMap, cipherword, candidate)

        # Intersect the new mapping with the existing intersected mapping:
        intersectedMap = intersectMappings(intersectedMap, candidateMap)

    # Remove any solved letters from the other lists:
    letterMapping = removeSolvedLettersFromMapping(intersectedMap)

    decryptedMessage = decryptWithCipherletterMapping(message,letterMapping)
    unSovledWords = findUnSovledWords(decryptedMessage)
    
    letterMapping = secondPass(unSovledWords,letterMapping,message)

    # Display the results to the user:
    

    return decryptWithCipherletterMapping(message, letterMapping)

def decryptWithCipherletterMapping(ciphertext, letterMapping):
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an _ underscore.

    # First create a simple sub key from the letterMapping mapping:
    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            # If there's only one letter, add it to the key.
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the ciphertext:
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'

    # Determine the possible valid ciphertext translations:
    print('Hacking...')
    print(hackSimpleSub(message))