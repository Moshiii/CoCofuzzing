import sys 
sys.path.append("..") 
import os

# setup:
testCodeDir = "../data/java-small/val_method_slice_1k5"
outputPath = "mergeFile_val_1k5.txt"
mergeCount = 1500

def mergeTestFile():
    with open(outputPath, "w+") as outputFile:
        for idx, fileName in enumerate(os.listdir(testCodeDir)):
            # print(idx, fileName)
            curTestPath = testCodeDir + os.sep + fileName
            with open(curTestPath, "r") as inputFile:
                line = inputFile.read()
                outputFile.write(line + "\n")
                inputFile.close()
            if idx >= mergeCount and mergeCount > 0:
                break
        outputFile.close()


if __name__ == '__main__':
    mergeTestFile()
