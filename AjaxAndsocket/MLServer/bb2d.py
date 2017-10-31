import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, report, training, utils, Variable
from chainer import datasets, iterators, optimizers, serializers
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
from chainer.dataset import concat_examples
from chainer.datasets import tuple_dataset
import random

class BinaryBoundary2D:
    def __init__(self, width, height, model):
        self.width = width
        self.height = height
        self.model = model
        
    def setDataset(self, datasetStr):
        self.rawTrainPos = []
        self.rawTrainT = []
        for line in datasetStr.split("\n"):
            vals = line.split(",")
            self.rawTrainPos.append([int(vals[0]),int(vals[1])])
            self.rawTrainT.append(int(vals[2]))
        self.rawTestPos = []
        self.rawTestT = []
        #TrainingDataからサンプルしてテストデータを作る
        for i in range(20):
            idx = random.randrange(0, len(self.rawTrainPos))
            self.rawTestPos.append(self.rawTrainPos[idx])
            self.rawTestT.append(self.rawTrainT[idx])
        self.trainPos, self.trainT = self.getNormalizedNpArray(self.rawTrainPos, self.rawTrainT)
        self.testPos, self.testT = self.getNormalizedNpArray(self.rawTestPos, self.rawTestT)
            
    def getNormalizedNpArray(self, rawPos, rawT):
        pos = np.array(rawPos, np.float32) / np.array([self.width, self.height], np.float32)
        t = np.array(rawT, np.int32)
        return pos, t
    
    def saveModel(fileName):
        serializers.save_npz(fileName,self.model)
    
    def loadModel(fileName):
        serializers.load_npz(fileName,self.model)

    def train(self, lr, maxEpoch):
        trainSet = tuple_dataset.TupleDataset(self.trainPos, self.trainT)
        testSet = tuple_dataset.TupleDataset(self.testPos, self.testT)
        
        trainIter = iterators.SerialIterator(trainSet, 1)
        testIter = iterators.SerialIterator(testSet, 1, repeat=False, shuffle=False)
        
        optimizer = optimizers.SGD(lr=lr)
        optimizer.setup(self.model)
        while trainIter.epoch < maxEpoch:
            #print(str(trainIter.epoch))
            trainBatch = trainIter.next()
            x, t = concat_examples(trainBatch)
            y = self.model(x)
            
            loss = F.softmax_cross_entropy(y, t)
            
            self.model.cleargrads()
            
            loss.backward()
            
            optimizer.update()
            
    def getY(self, x):
        return self.model(x)
        
    def getBoundary(self, interval=0.01):
        xx, yy = np.meshgrid(np.arange(0,1.0,interval), np.arange(0,1.0,interval))
        sampleMesh = np.array(np.c_[xx.ravel(), yy.ravel()], np.float32)
        
        y = self.getY(sampleMesh)
        
        predictLabel = F.argmax(y, axis=1).data
        
        return sampleMesh, predictLabel
            
        
       
