
import numpy as np
from enum import Enum 
import random 
import copy
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, RNN, Conv2D, MaxPooling2D, Flatten, Dropout
import keras
import time, datetime
from IPython.display import clear_output
from keras.models import model_from_json
import os

class NeuralNetwork:
    def __init__(self):
        self.model = Sequential()
        self.setup()
        self.features = None
        self.labels = None

    def csetup(self):
        self.model = Sequential()
        self.model.add(Conv2D(128, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=(9,9,2)))
        self.model.add(Conv2D(128, (3,3), activation='relu'))
        self.model.add(Conv2D(256, (2, 2), activation='relu'))
        self.model.add(Conv2D(384, (1, 1), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(3, 3)))
        self.model.add(Dropout(0.2))
        self.model.add(Flatten())
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(2, activation='softmax'))
    
        self.model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
    
    def setup(self):
        self.model.add(Dense(128,input_shape=(162,)))
        self.model.add(Activation('relu'))
        self.model.add(Dense(256))
        self.model.add(Activation('relu'))
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        self.model.add(Dense(256))
        self.model.add(Activation('relu'))
        self.model.add(Dense(128))
        self.model.add(Activation('relu'))
        self.model.add(Dense(2))
        self.model.add(Activation('softmax'))

        self.model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
    
    def train(self):
        if self.features is None or self.labels is None:
            print("Dude, you are missing data I think...")
            return
        self.model.fit(self.features, self.labels, epochs=10, batch_size=32)

    def set_data(self,features,labels):
        self.features = features
        self.labels = labels
    
    def predict(self,datum):
        return self.model.predict(datum)
    
    def set_model(self, model):
        self.model = model
    
    def save(self):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        # saving the model
        model_json = self.model.to_json()
        filename = "models/"+timestamp
        os.makedirs(filename, exist_ok=True)
        with open("models/"+timestamp+"/model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights("models/"+timestamp+"/weights.h5")
        print("Saved model to disk as with "+timestamp+" timestamp")
    
    def load(self, foldername):
        f = open("/home/welcomebuddy/Documents/projects/morganstanley/uttt_bot/tactics/model.json")
        model = model_from_json(f.read())
        f.close()
        model.load_weights("/home/welcomebuddy/Documents/projects/morganstanley/uttt_bot/tactics/weights.h5")
        # print("Model loaded from the disk")
        self.model = model
        # print("Model set to the Neural Network")