import numpy as np
import tensorflow as tf
import cv2
from keras.models import load_model
from My_Model import create_model


# model = create_model( 60 , 60 , 3 )
# model.load_weights('model_weights_RGB_O1_7600')

# # Convert the model.
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()

# # Save the model.
# with open('model.tflite', 'wb') as f:
#   f.write(tflite_model)



# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

image = [cv2.imread("./images_O1/data597.jpg") /255.]

# # Test the model on random input data.
# input_shape = input_details[0]['shape']
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)

input_data = np.array(image, dtype=np.float32)

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
check_pred = np.argmax(output_data)

print(output_data)
print(check_pred)

