import cv2
import numpy as np
import imutils
from keras.models import load_model
from preprocess import find_circle , find_top , find_square , BGR_to_Binary
from My_Model import create_model
from DataResult import addData , addData_SQLite
# from raspberry_GPIO import sevenSegment           # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# image = cv2.imread("image_Full_Menu/data20.jpg")
image = cv2.imread("image_Full_Menu/image_01.jpg")
# image = imutils.rotate(image, 180)
img = find_square(image)
top = find_top(img)
close , Circle_data = find_circle(top)

model = create_model( 60 , 60 , 1 )
model.load_weights('WeightModel')
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
    
    CData = BGR_to_Binary(Circle_data[i]) / 255.
    CData = np.expand_dims(CData, axis=0)
    # print(CData)
    w_pred = model.predict(CData)
    # AnsData[0] = model.predict(Circle_data[i])
    # print(i+1 ," = " , np.argmax(w_pred),"   ",w_pred)
    # print(np.ndarray.max(w_pred))
    if np.ndarray.max(w_pred) > 0.4 :            
        check_pred = np.argmax(w_pred) 
        # print(i+1 ," = " , check_pred,w_pred)
        if check_pred == 1 or check_pred == 2:
            # print(i+1)
            AnsData = addData(i,AnsData)
    # else:
    #     print(i+1 ," = " , 0 ,w_pred)

print(AnsData)
addData_SQLite(AnsData)   ### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# print(Circle_data.shape)

# TARGET_SIZE = (int(1984/2),int(928/2))
# close = cv2.resize(close,TARGET_SIZE)
# cv2.imshow('close', close)

# image = cv2.resize(image,TARGET_SIZE)
# cv2.imshow('image', image)

# top = cv2.resize(top,TARGET_SIZE)

# cv2.imshow('ori', Circle_data[23])
# cv2.imshow('ori24', Circle_data[24])
# cv2.imshow('top', BGR_to_Binary(Circle_data[23]))
# cv2.imshow('top24', BGR_to_Binary(Circle_data[24]))

# cv2.waitKey()