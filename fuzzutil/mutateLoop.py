import sys
sys.path.append("..")
from common import Common
from extractor import Extractor
from config import Config
from argparse import ArgumentParser
from fuzzutil.mutateData import MutateData
from fuzzutil import coverageInfo
from interactive_predict import InteractivePredictor
from model import Model
from fuzzutil.mutate_input_file import mutate_by_seq
import random
import numpy as np
import pickle
from tqdm import tqdm
import time
from fuzzutil.jarExtractor import JarExtractor

# need to set up
modelPath = "../models/java-large-model/model_iter52.release"
testDataPath = "mergeFile_test_1k5.txt"
tempSnippetPath = "tempSnippet.txt"
picklePath = "mutateResultResDict.pickle"
mutateSnippetPath = "mutateSnippetRes_test_1k5.txt"
successTotal = 1000

# const, just keep it
MAX_PATH_LENGTH = 8
MAX_PATH_WIDTH = 2
JAR_PATH = '../JavaExtractor/JPredict/target/JavaExtractor-0.0.1-SNAPSHOT.jar'
SHOW_TOP_CONTEXTS = 10
EXTRACTION_API = 'https://po3g2dx2qa.execute-api.us-east-1.amazonaws.com/production/extractmethods'

mutateResultResDict = {}
mutateSnippetList = []


def getConfig():
    parser = ArgumentParser()
    parser.add_argument("-d", "--data", dest="data_path",
                        help="path to preprocessed dataset", required=False)
    parser.add_argument("-te", "--test", dest="test_path",
                        help="path to test file", metavar="FILE", required=False)

    parser.add_argument("-s", "--save_prefix", dest="save_path_prefix",
                        help="path to save file", metavar="FILE", required=False)
    parser.add_argument("-l", "--load", dest="load_path",
                        help="path to saved file", metavar="FILE", required=False)
    parser.add_argument('--release', action='store_true',
                        help='if specified and loading a trained model, release the loaded model for a smaller model '
                             'size.')
    parser.add_argument('--predict', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--seed', type=int, default=239)
    args = parser.parse_args()
    args.predict = True
    args.load_path = modelPath
    config = Config.get_default_config(args)
    return config


def recordMutateResult(snippetIdx, seq, mutateSnippetIdx, neuronActive, neuronTotal, tagOriginal, tagPredict):
    curInfo = {"seq": seq.copy(), "mutateSnippetIdx": mutateSnippetIdx, "neuronActive": neuronActive,
               "neuronTotal": neuronTotal, "tagOriginal": str(tagOriginal).split("|"), "tagPredict": tagPredict}
    if snippetIdx in mutateResultResDict.keys():
        mutateResultResDict[snippetIdx].append(curInfo)
    else:
        mutateResultResDict.setdefault(snippetIdx, [curInfo])


def saveMutateResult():
    with open(picklePath, 'wb') as f1:
        pickle.dump(mutateResultResDict, f1)
        f1.close()
    with open(mutateSnippetPath, 'w') as f2:
        for snippet in mutateSnippetList:
            f2.write(snippet + "\n")
        f2.close()


def mainMutateLoop():
    config = getConfig()
    model = Model(config)
    print('Created model')
    # path_extractor = Extractor(config, EXTRACTION_API, config.MAX_PATH_LENGTH, max_path_width=2)
    path_extractor = JarExtractor(config, jar_path=JAR_PATH, max_path_length=MAX_PATH_LENGTH,
                                   max_path_width=MAX_PATH_WIDTH)
    dataSet = MutateData(testDataPath)
    dataSize = dataSet.getSnippetCount()
    successCounter = 0
    lastSuccessIdx = -1
    pbar = tqdm(range(dataSize))
    # for dataIdx in range(0, dataSize):
    for dataIdx in pbar:
        # pbar.set_description("Processing %s" % dataIdx)
        if successCounter > successTotal:
            print("finish!")
            break
        pbar.set_description("success:%s fail:%s" % (successCounter, dataIdx - successCounter))
        seq = []
        nc_rate = 0
        nc_rate_last_step = 0
        for naturalness_counter in list(range(4)):
            # naturalness_counter == 0  pass , no mutation
            if naturalness_counter != 0:
                seq.append(random.choice(['a', 'b', 'c', 'd', 'e', "f", "g", "h", "i", "j"]))
            # print(seq)
            codeSnippet = dataSet.getSnippetByIdx(dataIdx).strip()
            if codeSnippet == "":
                continue
            mutateSnippet = mutate_by_seq(codeSnippet, seq)
            # print(mutateSnippet)
            # nc_rate_last_step = nc_rate
            with open(tempSnippetPath, "w") as f:
                f.write(mutateSnippet)
                f.close()
            try:
                # predict_lines, pc_info_dict = path_extractor.extract_paths(mutateSnippet)
                predict_lines, pc_info_dict = path_extractor.extract_paths(tempSnippetPath)
                # print(predict_lines)
                # print(pc_info_dict)
            # except ValueError or TimeoutError:
            except Exception as e:
                # print(e)
                # print("original Snippet:", codeSnippet)
                # print("mutate Snippet:", mutateSnippet)
                if len(seq) != 0:
                    seq.pop()
                continue
            if len(predict_lines) != 1:
                print("len of predict_lines != 1")
                print("original Snippet:", codeSnippet)
                print("mutate Snippet:", mutateSnippet)
                if len(seq) != 0:
                    seq.pop()
                continue

            predict_lines = processRes(predict_lines[0])
            predict_lines = [predict_lines]

            [model_results, midoutTensorList] = model.predict2(predict_lines)
            if len(midoutTensorList) == 1:
                print("midoutTensorList is empty!")
                print("original Snippet:", codeSnippet)
                print("mutate Snippet:", mutateSnippet)
                if len(seq) != 0:
                    seq.pop()
                continue
            if lastSuccessIdx != dataIdx:
                successCounter += 1
                lastSuccessIdx = dataIdx
            prediction_results = Common.parse_results(model_results, pc_info_dict, topk=SHOW_TOP_CONTEXTS)
            curCoverageVec = coverageInfo.getCoverage(midoutTensorList)
            if naturalness_counter == 0:
                unionCoverageVec = curCoverageVec
            else:
                unionCoverageVec = coverageInfo.getCoverageVecUnion(unionCoverageVec, curCoverageVec)
            for index, method_prediction in prediction_results.items():
                # print('Original name:\t' + method_prediction.original_name)
                tagOriginal = method_prediction.original_name
                # print('Predicted:\t%s' % [step.prediction for step in method_prediction.predictions])
                tagPredict = [step.prediction for step in method_prediction.predictions]
            # print("totalActNum", np.sum(unionCoverageVec))
            # print("totalNeuronNum", unionCoverageVec.shape[-1])
            # print("totalRate", 100 * np.sum(unionCoverageVec) // unionCoverageVec.shape[-1])
            nc_rate = np.sum(unionCoverageVec) / unionCoverageVec.shape[-1]
            if nc_rate > nc_rate_last_step and naturalness_counter > 0:
                mutateSnippetList.append(mutateSnippet)
                mutateSnippetIdx = len(mutateSnippetList) - 1
                recordMutateResult(dataIdx, seq, mutateSnippetIdx, np.sum(unionCoverageVec), unionCoverageVec.shape[-1],
                                   tagOriginal, tagPredict)
            if naturalness_counter > 1 and nc_rate <= nc_rate_last_step:
                seq.pop()
            nc_rate_last_step = nc_rate
        if lastSuccessIdx != dataIdx:
            successCounter += 1
        
    saveMutateResult()


def processRes(line):
    max_data_contexts = 1000
    max_contexts = 200
    max_contexts_to_sample = max_contexts
    parts = line.rstrip('\n').split(' ')
    target_name = parts[0]
    contexts = parts[1:]

    if len(contexts) > max_contexts_to_sample:
        contexts = np.random.choice(contexts, max_contexts_to_sample, replace=False)

    csv_padding = " " * (max_data_contexts - len(contexts))
    returnStr = target_name + ' ' + " ".join(contexts) + csv_padding
    return returnStr


if __name__ == '__main__':
    mainMutateLoop()
    # printTrain()
