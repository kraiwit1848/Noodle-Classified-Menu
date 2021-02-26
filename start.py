import cv2
import numpy as np
import imutils
from keras.models import load_model
from preprocess import find_circle , find_top , find_square
from My_Model import create_model
from DataResult import addData , addData_SQLite
# from raspberry_GPIO import sevenSegment           # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# image = cv2.imread("image_Full_Menu/data20.jpg")
image = cv2.imread("image_Full_Menu/image_91.jpg")
# image = imutils.rotate(image, 180)
img = find_square(image)
top = find_top(img)
close , Circle_data = find_circle(top)

model = create_model( 60 , 60 , 3 )
model.load_weights('model_weights_RGB_O1_7600')
# ANS = model.predict(Circle_data)
# print(ANS)
# answer = [0,1,2,3,"ต้มยำ","หม่าล่า","ต้มยำ","น้ำใส",
# "น้ำเงี้ยว","น้ำยาป่า","ต้มยำ","ทรงเครื่อง","ยำพริกเผา","เส้นมาม่า","เส้นบะหมี่","เส้นบะหมี่หยก","เส้นราเมง",
# "เส้นเล็ก","เส้นใหญ่","ปกติ","พิเศษ","จัมโบ้",1,1,1]

# usd check position in answer
    
# AnsData = [ Menu , Spicy , Vegetable , Restaurant , Price ]

AnsData = [ "" , 1 , 1 , 1 , 45 ]
# AnsData_Index = 0

for i in range(25):
    
    Circle_data[i] = Circle_data[i] / 255.
    Circle_data[i] = np.expand_dims(Circle_data[i], axis=0)
    w_pred = model.predict(Circle_data[i])
    # AnsData[0] = model.predict(Circle_data[i])
    # print(i+1 ," = " , np.argmax(w_pred),"   ",w_pred)
    check_pred = np.argmax(w_pred)
    # print(i+1 ," = " , check_pred)

    # if check_pred == 1 : # version 1 is have 3 classify
    if check_pred == 1 or check_pred == 2: # version 2 is have 4 classify
        # print(i+1)
        AnsData = addData(i,AnsData)

print(AnsData)
addData_SQLite(AnsData)

# print(Circle_data.shape)

# TARGET_SIZE = (int(1984/2),int(928/2))
# close = cv2.resize(close,TARGET_SIZE)
# cv2.imshow('close', close)

# image = cv2.resize(image,TARGET_SIZE)
# cv2.imshow('image', image)

# top = cv2.resize(top,TARGET_SIZE)
# cv2.imshow('top', top)

# cv2.waitKey()