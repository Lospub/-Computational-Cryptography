import os, sys, util, detectEnglish, cryptomath, caesar_cipher_3, column_traspotation, assign4_affine
import itertools

SILENT_MODE = True

def combin():
    keyList = []
    for subset in itertools.permutations(range(1,3), 2):
        keyList.append(subset)
    for subset in itertools.permutations(range(1,4), 3):
        keyList.append(subset)
    for subset in itertools.permutations(range(1,5), 4):
        keyList.append(subset)
    for subset in itertools.permutations(range(1,6), 5):
        keyList.append(subset) 
    for subset in itertools.permutations(range(1,7), 6):
        keyList.append(subset)
    for subset in itertools.permutations(range(1,8), 7):
        keyList.append(subset)
    for subset in itertools.permutations(range(1,9), 8):
        keyList.append(subset)
    for subset in itertools.permutations(range(1,10), 9):
        keyList.append(subset)
    return keyList

def hacker(cipherType, ciphertext):
    if cipherType == 'caesar':
        file = open("dictionary.txt", "r")
        keyRange = file.read().splitlines()
        file.close()
    elif cipherType == 'transposition':
        keyRange = combin()
    elif cipherType == 'affine':
        keyRange = range(len(assign4_affine.SYMBOLS) ** 2)    
    else:
        print("Unknown cipher type: %s" % cipherType)
        sys.exit()

    print('Hacking...')
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')    
    
    for key in keyRange:
        if cipherType == 'caesar':
            decrypted = caesar_cipher_3.decrypt(ciphertext, key)            
        elif cipherType == 'transposition':
            decrypted = column_traspotation.decryptMessage(key, ciphertext)
        elif cipherType == 'affine':
            decrypted = assign4_affine.affine(key, ciphertext)
        if not SILENT_MODE:
            print('Tried Key %s... (%s)' % (key, decrypted[:40]))
        
        if detectEnglish.isEnglish(decrypted):
            print("\nfor line %s" % ciphertext)
            # print('Possible encryption hack:')
            print('Key %s: %s' % (key, decrypted[:200]))
            '''
            print('\nEnter D for done, or press Enter')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decrypted
            '''
    return None    
    
    
def main():
    ciphertexts = util.getTextFromFile().split('\n')
    
    
    cipherType = 'transposition'
    if len(sys.argv) > 2:
        cipherType = sys.argv[2]
    
    for line in ciphertexts:
        hackedMessage = hacker(cipherType, line)

    if hackedMessage == None:
        print('Failed to hack encryption.')
    else:
        print(hackedMessage)

if __name__ == '__main__':
    main()

