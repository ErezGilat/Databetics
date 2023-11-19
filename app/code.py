import pandas as pd
from pickle import load
import numpy as np


def scaling_func(data):
    scaler = load(open('./DATA/scaler-v1.pickle', 'rb'))
    return scaler.transform(data)


def diagnose(data):
    model = load(open('./DATA/model-v1.pickle', 'rb'), encoding='bytes')
    data = pd.DataFrame(data).convert_dtypes(np.int64)
    # print(model.predict(scaling_func(data)))
    return model.predict(scaling_func(data))
