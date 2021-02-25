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


# file = "O1"
file = "000"

BATCH_SIZE = 200
IMAGE_SIZE = (60,60)

dataframe = pd.read_csv('Data_ANS_'+file+'.csv', delimiter=',', header=0)

datagen = ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_dataframe(
    dataframe=dataframe.loc[0:1700],
    directory='images_'+file,
    x_col='FileName',    
    y_col='Class',
    color_mode='grayscale',
    shuffle=True,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='other')

validation_generator = datagen.flow_from_dataframe(
    dataframe=dataframe.loc[1701:1952],
    directory='images_'+file,
    x_col='FileName',
    y_col='Class',    
    color_mode='grayscale',
    shuffle=False,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='other')

model = create_model(IMAGE_SIZE[0],IMAGE_SIZE[1],1)
# inputIm = Input(shape = (IMAGE_SIZE[0],IMAGE_SIZE[1],1))
# conv1 = Conv2D(64,3,activation='relu',padding = 'same')(inputIm)
# pool1 = MaxPool2D()(conv1)
# conv2 = Conv2D(128,3,activation='relu',padding = 'same')(pool1)
# # conv2 = BatchNormalization()(conv2)
# # conv2 = Dropout(0.25)(conv2)
# pool2 = MaxPool2D()(conv2)

# conv3 = Conv2D(256,3,activation='relu',padding = 'same')(pool2)
# # conv3 = BatchNormalization()(conv3)
# conv3 = Dropout(0.25)(conv3)
# pool3 = MaxPool2D()(conv3)

# conv4 = Conv2D(128,3,activation='relu',padding = 'same')(pool3)
# # conv4 = Conv2D(64,3,activation='relu',padding = 'same')(conv4)
# conv4 = Dropout(0.25)(conv4)
# # conv4 = Dropout(0.25)(conv4)
# pool4 = MaxPool2D()(conv4)

# # conv5 = Conv2D(64,3,activation='relu',padding = 'same')(pool4)
# # conv5 = Dropout(0.25)(conv5)
# # pool5 = MaxPool2D()(conv5)

# flat = Flatten()(pool4)
# dense1 = Dense(512,activation='relu')(flat)
# dense1 = Dropout(0.5)(dense1)
# dense1 = Dense(256,activation='relu')(dense1)
# dense1 = Dropout(0.5)(dense1)
# predictedW = Dense(4,activation='sigmoid')(dense1)

# model = Model(inputs=inputIm, outputs=predictedW)


model.summary()

# model.compile(optimizer = Adam(lr = 1e-4),
#               loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#               metrics = ['accuracy'])

# model.save('project_model')



#Train Model

checkpoint = ModelCheckpoint('model_weights_binary_'+file, verbose=1, save_weights_only=True,monitor='val_accuracy',save_best_only=True, mode='max')
# print(len(train_generator),len(validation_generator))
model.fit_generator(
    train_generator,
    steps_per_epoch= len(train_generator),
    epochs=60, 
    validation_data=validation_generator,
    validation_steps= len(validation_generator),
    callbacks=[checkpoint])