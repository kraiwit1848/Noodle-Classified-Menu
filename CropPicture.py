import cv2
import imutils
import numpy as np

# ============================ crop picture =====================================

for i in range(1,4):
    img = cv2.imread('Data set/New/data'+str(i)+'.jpg')

    numberfile = i
    image_number = 1
    w = h = 70
    y = 315
    # x = 270
    for j in range(1,26):
    # for i in range(1,2):
        # y = 315
        x = 270
        for k in range(1,25):
            imcrop = img[y:y+h,x:x+w]
            imcrop = cv2.resize(imcrop,(46,46))
            # print(image_number,imcrop.shape)
            cv2.imwrite('Data set/New/'+str(numberfile)+'/data'+str(numberfile)+'{}.jpg'.format(image_number), imcrop)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 1)
            # cv2.putText(img, str(image_number) ,(x,y),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),4)
            image_number += 1
            x = x + 85
        y = y + 86


    img = imutils.rotate(img, 180)
    w = h = 70
    # x = 188
    y = 280

    for j in range(1,10):
    # for i in range(1,2):
        x = 188
        # y = 280
        for k in range(1,25):
            imcrop = img[ y:y+h,x:x+w]
            imcrop = cv2.resize(imcrop,(46,46))
            # print(image_number,imcrop.shape)
            cv2.imwrite('Data set/New/'+str(numberfile)+'/data'+str(numberfile)+'{}.jpg'.format(image_number), imcrop)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 2)
            # cv2.putText(img, str(image_number) ,(x,y),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),4)            
            image_number += 1
            x = x + 85
        y = y + 86
print("OK")
# ===============================================================================

# print(img.shape)
# TARGET_SIZE = (int(3507/5),int(2481/3))

# img = cv2.resize(img,TARGET_SIZE)
# cv2.imshow('image', img)

# cv2.waitKey()