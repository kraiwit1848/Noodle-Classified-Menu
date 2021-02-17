import tensorflow
from keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input, BatchNormalization, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import Adam

def create_model(shapeX,shapeY,color):
    inputIm = Input(shape = (shapeX,shapeY,color))
    conv1 = Conv2D(128,3,activation='relu',padding = 'same')(inputIm)
    pool1 = MaxPool2D()(conv1)
    conv2 = Conv2D(256,3,activation='relu',padding = 'same')(pool1)
    pool2 = MaxPool2D()(conv2)
    conv3 = Conv2D(512,3,activation='relu',padding = 'same')(pool2)
    conv3 = Dropout(0.25)(conv3)
    conv3 = Conv2D(256,3,activation='relu',padding = 'same')(conv3)
    conv3 = Dropout(0.25)(conv3)
    pool3 = MaxPool2D()(conv3)
    conv4 = Conv2D(128,3,activation='relu',padding = 'same')(pool3)
    conv4 = Dropout(0.25)(conv4)
    pool4 = MaxPool2D()(conv4)
    flat = Flatten()(pool4)
    dense1 = Dense(512,activation='relu')(flat)
    dense1 = Dropout(0.7)(dense1)
    dense1 = Dense(256,activation='relu')(dense1)
    dense1 = Dropout(0.5)(dense1)
    predictedW = Dense(4,activation='sigmoid')(dense1)

    model = Model(inputs=inputIm, outputs=predictedW)
    model.compile(optimizer = Adam(lr = 1e-4), loss = tensorflow.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics = ['accuracy'])

    return model
