import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from keras.models import load_model
from pandas.io.parsers import read_csv
from sklearn.utils import shuffle

import tensorflow as tf 
tf.reset_default_graph() 

def load_data(test=False):
    FTRAIN = '/home/devilshacker/ecommerce/src/facedetection/training.csv'
    FTEST = '/home/devilshacker/ecommerce/src/facedetection//test.csv'
    fname = FTEST if test else FTRAIN
    df = read_csv(os.path.expanduser(fname)) 
    df['Image'] = df['Image'].apply(lambda im: np.fromstring(im, sep=' '))
    df = df.dropna()
    
    X = np.vstack(df['Image'].values) / 255.
    X = X.astype(np.float32)
    X = X.reshape(-1, 96, 96, 1) 
    
    if not test:
        y = df[df.columns[:-1]].values
        y = (y - 48) / 48  
        X, y = shuffle(X, y, random_state=42)  # shuffle train data
        y = y.astype(np.float32)
    else:
        y = None
        
    return X,y