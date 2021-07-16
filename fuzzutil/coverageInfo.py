# import tensorflow as tf
import sys 
sys.path.append("..") 
import numpy as np


def getCoverage(tensorList, batchSize=1, threshold=0.4):
    # activateCondition = []
    activateVec = []
    active = 1
    for layerIdx, tensor in enumerate(tensorList):
        # print("inputShape:", tensor.shape)
        scaleTensor = scale2(tensor)
        # print("scaleShape:", scaleTensor.shape)
        # print("scaleMax:", scaleTensor.max())
        # print("scaleMin:", scaleTensor.min())
        # actRes = np.int64(scaleTensor > threshold)
        curActiveVec = []
        # print("scale max:", scaleTensor.max())
        # print("scale min:", scaleTensor.min())
        tempCount = 0
        for neuron_idx in range(scaleTensor.shape[-1]):
            if tempCount < 20:
                # print(np.mean(scaleTensor[..., neuron_idx]))
                tempCount += 1
            if np.mean(scaleTensor[..., neuron_idx]) > threshold:
                curActiveVec.append(1)
            else:
                curActiveVec.append(0)
        curActiveVec = np.array(curActiveVec, dtype=np.int64)
        # tempTensor = scaleTensor.reshape(-1, scaleTensor.shape[-1])
        # tempMean = np.mean(tempTensor, axis=0)
        # print("count1:", sum(curActiveVec))
        # print("count2:", sum(np.int64(tempMean > threshold)))
        # bins = np.linspace(0, 1, 11)
        # # print(bins)
        # binRes = np.digitize(tempMean, bins)
        # # print(binRes)
        # print("bin result")
        # for binIdx in range(1, 11):
        #     print("binIdx 0." + str(binIdx - 1) + "~0." + str(binIdx) + ":",
        #           np.extract(binRes == binIdx, binRes).shape[0])
        activateVec.append(curActiveVec)
    finalActiveRes = np.concatenate(activateVec, axis=0)
    return finalActiveRes


def scale(tensor):
    batchSize = tensor.shape[0]
    upper = np.max(tensor, axis=1)  # (batchsize, 1)
    lower = np.min(tensor, axis=1)  # (batchsize, 1)
    # print("upper:", upper)
    # print("lower:", lower)
    minus = lower.repeat(tensor.shape[-1]).reshape(batchSize, tensor.shape[-1])  # (batchsize, NeuronNum)
    divide = upper - lower  # (batchsize, 1)
    divide = divide.repeat(tensor.shape[-1]).reshape(batchSize, tensor.shape[-1])  # (batchsize, NeuronNum)
    scaleTensor = tensor - minus  # (batchsize, NeuronNum)
    scaleTensor = scaleTensor / divide  # (batchsize, NeuronNum)
    return scaleTensor


def getCoverageVecUnion(vecOld, vecNew):
    vecUnion = vecOld + vecNew
    return np.int64(vecUnion > 0)


def scale2(layer_outputs, rmax=1, rmin=0):
    '''
    scale the intermediate layer's output between 0 and 1
    :param layer_outputs: the layer's output tensor
    :param rmax: the upper bound of scale
    :param rmin: the lower bound of scale
    :return:
    '''
    divider = (layer_outputs.max() - layer_outputs.min())
    if divider == 0:
        return np.zeros(shape=layer_outputs.shape)
    X_std = (layer_outputs - layer_outputs.min()) / divider
    X_scaled = X_std * (rmax - rmin) + rmin
    return X_scaled


if __name__ == '__main__':
    # test = [[[1, 1, 1, 5, 10], [1, 1, 1, 10, 10]], [[12, 3, 4, 5, 3], [8, 9, 1, 12, 5]]]
    # test = [[range(0, 11)]]
    # a = np.array(test)
    # print(a)
    # print(a.shape)
    # print(getCoverage([a]))
    a = [[1, 2, 3, 1, 2, 3], [6, 4, 2, 1, 2, 3], [6, 9, 3, 1, 2, 3]]
    b = [[1, 2, 3], [6, 4, 2], [6, 9, 3]]
    a = np.array(a)
    b = np.array(b)
    # print(getCoverage([a, b]))
    print(print(np.mean(a, axis=0)))
