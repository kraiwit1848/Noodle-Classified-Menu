import cv2
import numpy as np
import tensorflow as tf
import imutils
import timeit
import os
from My_Model import create_model
from keras.models import load_model
from picamera import PiCamera
from preprocess import find_circle , find_top , find_square , BGR_to_Binary
from DataResult import addData , addData_SQLite
from raspberry_GPIO import Motion_sensor , Set_Pin 

def temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=","").replace("'C",""))
file = open("Data_test_Lite.txt","w")

Set_Pin()
camera = PiCamera()
camera.resolution = ( 1984 , 928 )

for RunLoop in range(100):
    start_temp = temp()
    start_time = timeit.default_timer()


    # ================ start ============================
    camera.capture('images/data.jpg')
    image = cv2.imread("images/data.jpg")
    img = find_square(image)
    top = find_top(img)
    close , Circle_data = find_circle(top)

    before_predict = timeit.default_timer() - start_temp        ################################

    model = create_model( 60 , 60 , 1 )
    model.load_weights('WeightModel')

    AnsData = [ "" , 1 , 1 , 1 , 45 ]

    for i in range(25):
        
        CData = BGR_to_Binary(Circle_data[i]) / 255.
        CData = np.expand_dims(CData, axis=0)
        w_pred = model.predict(CData)
        
        if np.ndarray.max(w_pred) > 0.4 :            
            check_pred = np.argmax(w_pred) 
            # print(i+1 ," = " , check_pred,w_pred)
            if check_pred == 1 or check_pred == 2:
                # print(i+1)
                AnsData = addData(i,AnsData)
        # else:
        #     print(i+1 ," = " , 0 ,w_pred)

    print(AnsData)
    
    before_InsertData = timeit.default_timer() - start_temp  ################################

    addData_SQLite(AnsData)  # <<<<<<<<<<<<<<<< 

    # ================ end ================================================

    end_temp = temp()
    RunTime = timeit.default_timer() - start_time

    file.write(str(RunLoop + 1) + ","+str(before_predict)+ ","+str(before_InsertData)+ ","+str(RunTime)+ ","+str(start_temp)+ ","+str(end_temp))

file.colse()