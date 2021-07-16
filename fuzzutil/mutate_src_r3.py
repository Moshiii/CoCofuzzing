import sys 
sys.path.append("..") 
import os
import fuzzutil.mutate_input_file as mu
import random

# setup:
testCodeDir = "/mnt/d/code/code2vec-master/data/rq4/testing_ori_1k/split/"
outputPath = "/mnt/d/code/code2vec-master/data/rq4/testing_r3_mu_1k"
mergeCount = 1000

if not os.path.exists(outputPath):
    os.makedirs(outputPath)

def mergeTestFile():
    for idx, fileName in enumerate(os.listdir(testCodeDir)):
        # print(idx, fileName)
        curTestPath = testCodeDir + os.sep + fileName
        outTestPath = outputPath + os.sep +"mu_"+ fileName

        with open(curTestPath, "r") as inputFile:
            line = inputFile.read().replace('\n','')
            inputFile.close()
        
        line = mu.mutate_by_option(random.choice(['b', 'c', 'd', 'e', "f", "g", "h", "i"]), line)
        line = mu.mutate_by_option(random.choice(['b', 'c', 'd', 'e', "f", "g", "h", "i"]), line)
        line = mu.mutate_by_option(random.choice(['b', 'c', 'd', 'e', "f", "g", "h", "i"]), line)

        with open(outTestPath, "w") as outputFile:
            outputFile.write(line)

        if idx >= mergeCount and mergeCount > 0:
            break



if __name__ == '__main__':
    mergeTestFile()
