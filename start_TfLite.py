import cv2
import numpy as np
import tensorflow as tf
import imutils
# from keras.models import load_model
from preprocess import find_circle , find_top , find_square
# from My_Model import create_model
from DataResult import addData , addData_SQLite
# from raspberry_GPIO import sevenSegment           # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# image = cv2.imread("image_Full_Menu/data20.jpg")
image = cv2.imread("image_Full_Menu/image_01.jpg")
# image = imutils.rotate(image, 180)
img = find_square(image)
top = find_top(img)
close , Circle_data = find_circle(top)

# model = create_model( 60 , 60 , 3 )
# model.load_weights('model_weights_RGB_O1_7600')

# # ANS = model.predict(Circle_data)
# # print(ANS)
# # answer = [0,1,2,3,"ต้มยำ","หม่าล่า","ต้มยำ","น้ำใส",
# # "น้ำเงี้ยว","น้ำยาป่า","ต้มยำ","ทรงเครื่อง","ยำพริกเผา","เส้นมาม่า","เส้นบะหมี่","เส้นบะหมี่หยก","เส้นราเมง",
# # "เส้นเล็ก","เส้นใหญ่","ปกติ","พิเศษ","จัมโบ้",1,1,1]

# # usd check position in answer
    
# # AnsData = [ Menu , Spicy , Vegetable , Restaurant , Price ]
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

AnsData = [ "" , 1 , 1 , 1 , 45 ]
# AnsData_Index = 0

for i in range(25):
    
    CircleD = [Circle_data[i] / 255.]

    # CircleD = np.expand_dims(CircleD, axis=0)

    input_data = np.array(CircleD, dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])


    # w_pred = model.predict(Circle_data[i])
    # check_pred = np.argmax(w_pred)

    check_pred = np.argmax(output_data)
    # print(i+1 ," = " , check_pred)

    # if check_pred == 1 : # version 1 is have 3 classify
    if check_pred == 1 or check_pred == 2: # version 2 is have 4 classify
        # print(i+1)
        AnsData = addData(i,AnsData)

print(AnsData)
# addData_SQLite(AnsData)  # <<<<<<<<<<<<<<<< 
