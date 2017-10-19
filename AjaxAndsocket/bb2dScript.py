# coding: utf-8
import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, report, training, utils, Variable
from chainer import datasets, iterators, optimizers, serializers
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
from chainer.training import extensions
from chainer.dataset import concat_examples
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
import random
from chainer.datasets import tuple_dataset
from bb2d import BinaryBoundary2D


def generate_cmap(colors):
    """自分で定義したカラーマップを返す"""
    values = range(len(colors))

    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)

# ## 別モデルの模索

# In[23]:

class SimpleModel(Chain):
    def __init__(self, n_out):
        super(SimpleModel, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, 100)
            self.l2 = L.Linear(None, 100)
            self.l3 = L.Linear(None, n_out)
                        
    def __call__(self, x):
        #層の結合結果に、活性化関数をかませる
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        y = self.l3(h2)
        return y


# In[24]:

def GetBoundary(txt, graphPrefix=""):
  bb2d = BinaryBoundary2D(300,300)
  bb2d.setDataset(txt.strip())
  bb2d.train(SimpleModel(2), 0.02, 240)

  mesh, pred = bb2d.getBoundary(0.015)
  cm = generate_cmap(['#FFFFFF', '#000000'])
  plt.scatter(mesh[:,0], mesh[:,1], c=pred, cmap=cm)

  cm = generate_cmap(['#EE5050', '#9090FF'])
  plt.scatter(bb2d.trainPos[:,0], bb2d.trainPos[:,1], c=bb2d.trainT, cmap=cm)

  plt.savefig("plot_"+graphPrefix)

  dataLen = pred.shape[0]
  preMatrix = np.empty((3, dataLen))
  preMatrix[0,:] = mesh.T[0,:]
  preMatrix[1,:] = mesh.T[1,:]
  preMatrix[2,:] = pred
  result = "\n".join([",".join([str(np.round(m[0],3)), str(np.round(m[1],3)), str(int(m[2]))]) for m in preMatrix.T])
  return result
