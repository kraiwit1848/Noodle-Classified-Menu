import cv2
import numpy as np
import tensorflow as tf
import imutils
import time
import timeit
import os
# from My_Model import create_model
# from keras.models import load_model
from picamera import PiCamera
from preprocess import find_circle , find_top , find_square , BGR_to_Binary
from DataResult import addData , addData_SQLite
from raspberry_GPIO import Motion_sensor , Set_Pin 

Set_Pin()
camera = PiCamera()
camera.resolution = ( 1984 , 928 )
Start = 0
print("start")
while True :

    if Start :
        try :
            print("start run")
            time.sleep(0.1)
            # ================ start ============================                        
            camera.capture('images/data.jpg')
            image = cv2.imread("images/data.jpg")
            img = find_square(image)
            top = find_top(img)
            close , Circle_data = find_circle(top)

            interpreter = tf.lite.Interpreter(model_path="model_Binary.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            AnsData = [ "" , 1 , 1 , 1 , 45 ]
            state = 1

            for i in range(25):
                
                CircleD = [ BGR_to_Binary(Circle_data[i]) / 255.]
                input_data = np.array(CircleD, dtype=np.float32).reshape(1,60,60,1)
                interpreter.set_tensor(input_details[0]['index'], input_data)
                interpreter.invoke()
                w_pred = interpreter.get_tensor(output_details[0]['index'])
                
                if np.ndarray.max(w_pred) > 0.80 :
                    check_pred = np.argmax(w_pred)       
                    # print(i+1 ," = " , check_pred,w_pred)
                    if check_pred == 1 or check_pred == 2:
                        AnsData = addData(i,AnsData)
                else:
                    state = 0  ### Used to require an accuracy of more than 80%.
                    # print(i+1 ," = " , 0 ,w_pred)
                    break

            if state :                    
                print(AnsData)
                addData_SQLite(AnsData)  # <<<<<<<<<<<<<<<< 
                Start = 0
            else:
                Start = 1

        except:
            Start = 1
    else :
        Start = Motion_sensor()

    # ================ end ================================================