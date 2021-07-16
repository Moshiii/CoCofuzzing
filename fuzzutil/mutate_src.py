import sys 
sys.path.append("..") 
import os
import fuzzutil.mutate_input_file as mu
import random
import sys

print(sys.argv)

folder = sys.argv[1]
option = sys.argv[2]
# setup:code2seq_orign\data\java-small
testCodeDir = "../data/java-small/test_ori_1k"
outputPath = "../data/java-small/"+folder
mergeCount = 1000

if not os.path.exists(outputPath):
    os.makedirs(outputPath)

def mutateFile():
    for idx, fileName in enumerate(os.listdir(testCodeDir)):
        # print(idx, fileName)
        curTestPath = testCodeDir + os.sep + fileName
        outTestPath = outputPath + os.sep +"mu_"+ fileName

        with open(curTestPath, "r") as inputFile:
            line_src = inputFile.read().replace('\n','')
            inputFile.close()
        
        line = mu.mutate_by_option(option, line_src)
        if idx >= mergeCount and mergeCount > 0:
            break
            
        if line =="":
            continue

        with open(outTestPath, "w") as outputFile:
            outputFile.write(line)


if __name__ == '__main__':
    mutateFile()
