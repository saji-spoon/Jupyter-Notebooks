import json
import os
import datetime
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
import numpy as np

from chainer import datasets, iterators, optimizers, serializers

def generate_cmap(colors):
    """自分で定義したカラーマップを返す"""
    values = range(len(colors))

    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)

def PlotTupleDataSet(tupledataset, colMap=["#FF8888", "#8888FF"], x=0, y=1):
    X = np.array([[dt[0][x] for dt in tupledataset],[dt[0][y] for dt in tupledataset]], np.float32).T
    y = np.array([dt[1] for dt in tupledataset], np.int32)
    cm = generate_cmap(colMap)
    plt.scatter(X[:,0], X[:,1], c=y, cmap = cm)

def PlotLossAndAccuracy(out, log_name):
    '''
    out ... Extension Output Directory (same as trainer's argument [out])
    log_name ... LogReport logfile (same as LogReport's argument [log_name])
    '''
    filePath = out+"/"+log_name
    
    ts = os.stat(filePath).st_mtime
    dt = datetime.datetime.fromtimestamp(ts)
    print(filePath)
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))
    
    f = open(filePath)
    json_data = json.load(f);
    f.close()

    arr_epoch = []
    arr_train_loss = []
    arr_train_accuracy = []
    arr_test_loss = []
    arr_test_accuracy = []

    for e in json_data:
        arr_epoch.append(e["epoch"])
        arr_train_loss.append(e["main/loss"])
        arr_train_accuracy.append(e["main/accuracy"])
        arr_test_loss.append(e["validation/main/loss"])
        arr_test_accuracy.append(e["validation/main/accuracy"])
        
    tmp = plt.xlabel('epoch')
    tmp = plt.ylabel('loss')
    tmp = plt.plot(arr_epoch, arr_train_loss)
    tmp = plt.plot(arr_epoch, arr_test_loss)
    plt.show()

    tmp = plt.xlabel('epoch')
    tmp = plt.ylabel('accuracy []')
    tmp = plt.plot(arr_epoch, arr_train_accuracy)
    tmp = plt.plot(arr_epoch, arr_test_accuracy)
    plt.show()

