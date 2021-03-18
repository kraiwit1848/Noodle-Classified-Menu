from keras.models import Model, load_model
from keras.layers import Dense, Dropout, Flatten, Input, BatchNormalization, Conv2D, MaxPool2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import Callback, ModelCheckpoint
# from keras.losses import SparseCategoricalCrossentropy
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from My_Model import create_model

import numpy as np
import cv2
from preprocess import BGR_to_Binary

file = "O1"
test_percen = 10
IMAGE_SIZE = (60,60)

# columns = ["FileName","Class0","Class1","Class2","Class3","Class4","Class"]
dataframe = pd.read_csv('Data_ANS_'+file+'.csv', delimiter=',', header=0)

in_train , out_train = [] , []
in_test , out_test = [] , []

# in_train
for i in dataframe['FileName'] :
    in_train.append( BGR_to_Binary( cv2.imread("images_"+file+"/"+i) ) )
# out_train
for i in dataframe["Class"] :
    split = i.split(",")
    out_train.append(np.array([float(split[0]),float(split[1]),float(split[2]),float(split[3]),float(split[4])]))

# in_test and out_test
for i in range( int(( len(in_train) / 100 ) * test_percen )):
    in_test.append(in_train.pop())
    out_test.append(out_train.pop())

# print("Data train: ", len(in_train) , "Data test", len(in_test) ," sum : ",len(in_train)+len(in_test))

in_train = np.uint16(in_train)
out_train = np.uint16(out_train)
in_test = np.uint16(in_test)
out_test = np.uint16(out_test)

in_train = in_train / 255.
in_test = in_test / 255.

print("Data train: ", len(in_train) , "Data test", len(in_test) ," sum : ",len(in_train)+len(in_test))



# create Model
model = create_model(IMAGE_SIZE[0],IMAGE_SIZE[1],1)
model.summary()

# >>>  !!! TRAIN START !!!  <<<
checkpoint = ModelCheckpoint('model_weights_'+file, verbose=1, save_weights_only=True,monitor='val_accuracy',save_best_only=True, mode='max')
model.fit(
    in_train,
    out_train,
    epochs = 60, 
    validation_data = (in_test , out_test),
    callbacks = [checkpoint])
