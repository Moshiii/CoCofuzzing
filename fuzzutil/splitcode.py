import sys 
sys.path.append("..") 

import os


# setup:
inputPath = "mutateSnippetRes.txt"
outputfolderPath = "../data/mergeFile_val_1k5/"
# mergeCount = 1500

def splitTestFile():
    
    with open(inputPath, 'r') as file:
        linelist = file.readlines()

    if not os.path.exists(outputfolderPath):
        os.makedirs(outputfolderPath)

    for idx in range(len(linelist)):
        with open(outputfolderPath + str(idx) +".java", "w+") as outputFile:
            outputFile.write(linelist[idx])

if __name__ == '__main__':
    splitTestFile()
