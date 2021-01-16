import os, sys, fileFreqAnalysis



LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'    


def evalFile(file1, file2):
    
    message1 = open(file1).read()
    message2 = open(file2).read()    
    mes1NoSymb = killSymb(message1)
    mes2NoSymb = killSymb(message2)
    # kill symbols
    lenMesNS = len(mes1NoSymb)  
    # length of no symbols
    
    mes1NoRept = killRept(mes1NoSymb)
    mes2NoRept = killRept(mes2NoSymb)
    # kill repeats
    lenMesNR = len(mes1NoRept)
    # length of no repeats
    
    
    numerKA = 0
    # numerator of Key Accuracy
    i = -1
    for e in mes1NoRept:
        i += 1
        if e == mes2NoRept[i]:
            numerKA += 1

    numerKD = 0
    # numerator of Dycipherment Accuracy
    i = -1
    for e in mes1NoSymb:
        i += 1
        if e == mes2NoSymb[i]:
            numerKD += 1

    ans = ['0','0']
    ans[0] = numerKA / lenMesNR
    ans[1] = numerKD / lenMesNS
    return ans
    
    
def killRept(string):
    strNew = ""
    for i in string:
        if i not in strNew:
            strNew += i
    return(strNew)


def killSymb(string):
    strNew = ""
    for i in string:
        if i.upper() in LETTERS:
            strNew += i
    return(strNew)


def main():
    #message1 = "this is an example"
    #message2 = "tsih ih an ezample"
    
    #filename = "1984"
    #plaintext = "text_" + filename + "_plain"
    #dyciphermenttext = "text_"+ filename + "_cipher_freqDecypt"
    
    #message1 = open(plaintext).read()
    #message2 = open(dyciphermenttext).read()
    #print(evalFile(message1, message2))
    a= evalFile('text_forest_cipher_freqDecypt', 'text_forest_plain')
    print(a)
main()
