import cv2
import numpy as np
import imutils
# from keras.models import load_model

def Mask_IMG(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 9)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    thresh = cv2.threshold(sharpen,0,150, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    return close



def find_square(image):
    close = Mask_IMG(image)
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    min_area = 10000
    # min_area = 100
    # image_number = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area:
            # print(area)           
            x,y,w,h = cv2.boundingRect(c)
            ROI = image[y:y+h, x:x+w]
            # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 5)
            # image_number += 1
    return ROI

def find_top(img,):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_rag = cv2.inRange(hsv,(70,100,1),(90,245,60))

    cnts = cv2.findContours(img_rag, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    min_area = 2500
    max_area = 4000
    x,y = 0,0
    for c in cnts:
        area = cv2.contourArea(c)
        # print(area)
        if min_area < area < max_area:
            # print(area)           
            x,y,w,h = cv2.boundingRect(c)
            # ROI = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 5)
    # print(x,y,img.shape)
    if x < img.shape[1]/2 :
        img = imutils.rotate(img, 180)

    return img

def find_circle(img):
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    low = 0
    high = 91
    blurred = cv2.inRange(img,(low,low,low),(high,high,high))
    blur = cv2.medianBlur(blurred, 5)

    minDist = 15
    param1 = 15 #500
    param2 = 15 #200 #smaller value-> more false circles
    minRadius = 14
    maxRadius = 20 #10

    # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    # count = 0
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles[0] = np.uint16(np.around(sorted(circles[0], key=lambda x: x[0])))
        
        if circles[0].shape[0] == 35 :
            row = []
            column = [4,3,3,3,3,3,3,3,3,4,3]
            check_count = 0
            for i in range(11):
                row.append([])
                for j in range(column[i]):
                    row[i].append(circles[0][check_count])
                    check_count += 1
                row[i] = np.uint16(np.around(row[i]))
                row[i] = np.uint16(np.around(sorted(row[i], key=lambda x: x[1])))

            circles_new = [[]]            
            for i in range(11):
                for j in range(column[i]):
                    circles_new[0].append(row[i][j])
            circles_new = np.uint16(np.around(circles_new))
            
            # print(circles_new[0])
        else :
            return False

        Circle_data = []
        # image_number = 0
        for i in circles_new[0,:]:
            # count += 1
            # cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 5)
            x,y,_ = i
            x = x - 23
            y = y - 23            
            ROI = img[y:y+46, x:x+46]
            ROI = imutils.rotate(ROI, 90)
            # ROI = cv2.resize(ROI,(75,75))
            Circle_data.append(ROI)
            # cv2.imwrite('test_save/ROI_{}.jpg'.format(image_number), ROI)
            # cv2.putText(img, str(count) ,(x,y),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0),5)
            # image_number += 1
        Circle_data = np.uint16(np.around(Circle_data))

    return img , Circle_data

image = cv2.imread("image_Full_Menu/image_24.jpg")
# image = imutils.rotate(image, 180)
img = find_square(image)
top = find_top(img)
close , Circle_data = find_circle(top)

# model = load_model('Miracle.h5')
# ANS = model.predict(Circle_data)
# print(ANS)

# print(Circle_data.shape)

# TARGET_SIZE = (int(1984/2),int(928/2))
# close = cv2.resize(close,TARGET_SIZE)
# cv2.imshow('close', close)

# image = cv2.resize(image,TARGET_SIZE)
# cv2.imshow('image', image)

# top = cv2.resize(top,TARGET_SIZE)
# cv2.imshow('top', top)

cv2.waitKey()