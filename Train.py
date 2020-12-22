from keras.models import Model, load_model
from keras.layers import Dense, Dropout, Flatten, Input, BatchNormalization, Conv2D, MaxPool2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import Callback, ModelCheckpoint
# from keras.losses import SparseCategoricalCrossentropy
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf

BATCH_SIZE = 300
IMAGE_SIZE = (75,75)

dataframe = pd.read_csv('Data_ANS.csv', delimiter=',', header=0)

datagen = ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_dataframe(
    dataframe=dataframe.loc[0:4000],
    directory='images',
    x_col='FileName',    
    y_col='Class',
    shuffle=True,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='other')

validation_generator = datagen.flow_from_dataframe(
    dataframe=dataframe.loc[4001:4500],
    directory='images',
    x_col='FileName',
    y_col='Class',
    shuffle=False,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='other')


inputIm = Input(shape = (75,75,3,))
conv1 = Conv2D(32,3,activation='relu',padding = 'same')(inputIm)
pool1 = MaxPool2D()(conv1)
conv2 = Conv2D(64,3,activation='relu',padding = 'same')(pool1)
pool2 = MaxPool2D()(conv2)
conv3 = Conv2D(128,3,activation='relu',padding = 'same')(pool2)
pool3 = MaxPool2D()(conv3)
conv4 = Conv2D(256,3,activation='relu',padding = 'same')(pool2)
pool4 = MaxPool2D()(conv4)
conv5 = Conv2D(128,3,activation='relu',padding = 'same')(pool2)
pool5 = MaxPool2D()(conv5)

flat = Flatten()(pool5)
dense1 = Dense(128,activation='relu')(flat)
dense1 = Dropout(0.5)(dense1)
dense1 = Dense(256,activation='relu')(dense1)
dense1 = Dropout(0.5)(dense1)
predictedW = Dense(4,activation='relu')(dense1)

model = Model(inputs=inputIm, outputs=predictedW)


model.summary()

model.compile(optimizer = Adam(lr = 1e-4),
              loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics = ['accuracy'])

# model.compile(optimizer = Adam(lr = 1e-4), loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics = ['accuracy'])

checkpoint = ModelCheckpoint('Miracle.h5', verbose=1, monitor='val_accuracy',save_best_only=True, mode='max')

#Train Model
model.fit_generator(
    train_generator,
    steps_per_epoch= len(train_generator),
    epochs=60, 
    validation_data=validation_generator,
    validation_steps= len(validation_generator),
    callbacks=[checkpoint])