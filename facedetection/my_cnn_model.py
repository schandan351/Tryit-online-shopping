from keras.models import Sequential,load_model
from keras.models import Sequential
from keras.layers import Convolution2D,MaxPooling2D,Flatten,Dense,Dropout
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

 

def get_my_cnn_model_architecture():
    model=Sequential()
    
    model.add(Convolution2D(32,(5,5),input_shape=(96,96,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Convolution2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))

    model.add(Convolution2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Convolution2D(30, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    
    #add flatten layer
    model.add(Flatten())
    
    model.add(Dense(64, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(64,activation='relu'))
    model.add(Dense(30))
       
    return model


def compile_my_cnn_model(model,optimizer,loss,metrics):
    model.compile(optimizer=optimizer,loss=loss,metrics=metrics)
    
def train_my_cnn_model(model,X_train,y_train):
    return model.fit(X_train,y_train,epochs=100,batch_size=300,verbose=1,validation_split=0.2)

def save_my_cnn_model(model,filename):
    model.save(filename+'.h5')
    
def load_my_cnn_model(filename):
    import tensorflow as tf 
    tf.reset_default_graph() 
    return load_model(filename+'.h5')


