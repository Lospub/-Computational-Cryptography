import re
import itertools,detectEnglish

ENG_LETT_FREQ= {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
NONLETTERS_PATTERN = re.compile('[^A-Z]')
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def getNthSubkeysLetters(nth, keylength, message):
    # Returns every nth letter for each keylength set of letters in text.
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
        i += keylength
    return ''.join(letters)

    
def vigenereKeySolver(ciphertext, keylength):
    ciphertext = ciphertext.upper()
    a = getSubIMC(ciphertext,keylength)
    keys = getsPossibleKeys(a,keylength)
    return keys


def calculateIMC(message):
#function:      
#           Calculate the IMC for given message
#Parameter (message): 
#          the given character text
#Return message: IMC
    IMC = 0
    length = len(message)
    for l in LETTERS:
        if l in message:
            IMC += (message.count(l)/length)*(ENG_LETT_FREQ[l]/100)  
    return IMC    

def getPossibleSubSequences(message):
#function:
#           get possible sequences for each letter
#parameter (message): 
#           given a letter message        
#return:
#           a list of possible ciphers by each letter.
    messages = []
    for key in range(len(LETTERS)):
        text = ''
        for c in message:
            idx = LETTERS.find(c)
            text += LETTERS[(idx - key) % 26]     #shiff left
        messages.append(text)
    return messages

def getIMCs(messages):  
#function:
#   get IMC for each possible sequences and return a sorted result
#parameter:
#   a list of possible messages enciphered by each letter.
#return:
#   a dictionary letter which sorts by IMC
    IMCs = {}
    idx = 0
    for msg in messages:
        IMCs[LETTERS[idx]] = calculateIMC(msg)
        idx += 1
    sortedIMCs = sorted(IMCs.items(),key = lambda x:x[1],reverse=True)
    return sortedIMCs


def getSubIMC(message,keylength):
#function:
#   Get IMC for each character of subsequence
#parameter:
#   message: a sequence characters.
#   keylenght: the lenght of key
#Return:
#   a list of (letter,IMC) for each sequences
    sequenList = []
    for i in range(keylength):
        subsequence = getNthSubkeysLetters(i+1, keylength, message)
        sq = getPossibleSubSequences(subsequence)
        IMCs = getIMCs(sq)
        sequenList.append(IMCs)
    return sequenList

#Based on IMCs to get possible keys
def getsPossibleKeys(IMCs,keylength):
    sortList = list(itertools.product(range(2), repeat=keylength))
    keys = {}
    j = 0
    for i in range(len(sortList)):
        key = ''
        count = 0
        for k in sortList[i]:
            key += IMCs[j][k][0]
            j += 1
            j %= keylength       
        keys[key] = count
    sorted_key = sorted(keys.items(), key=lambda kv: kv[1], reverse=True)
    keyList = []
    countt = 0
    for i in sorted_key:
        if countt < 10:
            keyList.append(i[0])
            countt += 1
        else:
            break    
    return keyList[:10]


def hackVigenere(ciphertext):
    keylengths = keyLengthIC(ciphertext,10)
    keys = []
    freqScores = []
    for kl in keylengths:
        possibleKeys = vigenereKeySolver(ciphertext,kl)
        for key in possibleKeys:
            decryptedText = translateMessage(key, ciphertext, 'decrypt')
            scores =(key,detectEnglish.getEnglishCount(decryptedText))
            freqScores.append(scores)
            if detectEnglish.isEnglish(decryptedText):
                return key
    #if I do not find a most accurate key.
    return(sorted(freqScores, key=lambda x: x[1],reverse=True)[:1][0])

def crackPassword():
    f = open('password_protected.txt')
    ciphertext = f.read()
    key = hackVigenere(ciphertext)
    decryptedText = translateMessage(key, ciphertext, 'decrypt')
    print(decryptedText)
    f.close()

#Function from assignment 6
def stringIC(inputstr):
    N = len(inputstr)
    C = list(set(inputstr))
    nominator = 0
    for c in C:
        f = inputstr.count(c)
        nominator = nominator + (f*(f-1))
    if N <= 1:
        return 0
    else:
        return nominator/(N*(N-1))


def subseqIC(ciphertext, keylen):
    IC = 0
    for i in range(1,keylen+1):
        pattern = getNthSubkeysLetters(i,keylen,ciphertext)
        IC = IC +stringIC(pattern)
    if keylen == 0:
        return 0
    else:
        return IC/keylen

def keyLengthIC(ciphertext, n):
    ICs = []
    for i in range(1,20+1):
        IC = subseqIC(ciphertext,i)
        t =(i,IC)
        ICs.append(t)
    keys = [k[0] for k in (sorted(ICs, key=lambda x: x[1],reverse=True))]  
    return keys[:n]

def translateMessage(key, message, mode):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS.
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # Add if encrypting.
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex]) # Subtract if decrypting.

            num %= len(LETTERS) # Handle any wraparound.

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)
    return ''.join(translated)


#ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
#best_keys = vigenereKeySolver(ciphertext, 5)
#ciphertext = "A'q nrxx xst nskc epu qr uet zw ggx yfvdari, js B figu xh xmpu wheiqei mg xcbi fw xq nskc. Hkeslsytj fxueov iqlmptx t nitp phfk vzqx skq. Z gtf xgcp bl mu ymf tc vyi psc jv wiwemj Lx uswch ggx ucixh fgtenki qw xaw rqzwx gyvjmww lkj abfhqn."
#key = hackVigenere(ciphertext)
##assert key == "SECRET"

#ciphertext = "XUOD QK H WRTEMFJI JOEP EBPGOATW JSZSZV OVVQY JWMY JHTNBAVR GU OMLLGG KYODPWU YSWMSH OK ZSSF AVZS BZPW"
#key = hackVigenere(ciphertext)
#print(key)

ciphertext = "QPWKALVRXCQZIKGRBPFAEOMFLJMSDZVDHXCXJYEBIMTRQWNMEAIZRVKCVKVLXNEICFZPZCZZHKMLVZVZIZRRQWDKECHOSNYXXLSPMYKVQXJTDCIOMEEXDQVSRXLRLKZHOV"
best_keys = vigenereKeySolver(ciphertext, 5)
print(best_keys)
assert best_keys[0] == "EVERY"