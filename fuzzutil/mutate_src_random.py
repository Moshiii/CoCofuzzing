import sys 
sys.path.append("..") 
import os
import fuzzutil.mutate_input_file as mu
import random
import sys

print(sys.argv)

folder = sys.argv[1]
times = sys.argv[2]
# setup:
# testCodeDir = "../../code2vec-master/data/java-small/train_ori_10k"
# outputPath = "../../code2vec-master/data/java-small/"+folder
testCodeDir = "../data/java-small/train_ori_10k"
outputPath = "../data/java-small/"+folder
mergeCount = 10000

if not os.path.exists(outputPath):
    os.makedirs(outputPath)

def mutateFile():
    for idx, fileName in enumerate(os.listdir(testCodeDir)):
        # print(idx, fileName)
        curTestPath = testCodeDir + os.sep + fileName
        outTestPath = outputPath + os.sep +"mu_"+times+"_"+ fileName

        with open(curTestPath, "r") as inputFile:
            line = inputFile.read().replace('\n','')
            inputFile.close()
        for s in range(int(times)):
            line = mu.mutate_by_option(random.choice(['a','b', 'c', 'd', 'e', "f", "g", "h", "i",'j']), line)

        with open(outTestPath, "w") as outputFile:
            outputFile.write(line)

        if idx >= mergeCount and mergeCount > 0:
            break

if __name__ == '__main__':
    mutateFile()
