import cv2
import numpy as np
import imutils
# from keras.models import load_model



def find_square(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    BGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    hsv = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)
    _ , in_range = cv2.threshold(hsv,75,255,cv2.THRESH_BINARY)
    # in_range = cv2.cvtColor(in_range, cv2.COLOR_GRAY2RGB)
    # in_range = cv2.cvtColor(in_range, cv2.COLOR_GRAY2RGB)
    new_in_range = cv2.inRange(in_range,(0,0,100),(0,0,255))
    blur = cv2.medianBlur(new_in_range, 3)

    # close = Mask_IMG(image)    
    cnts = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    min_area = 500000
    max_area = 2000000
    # min_area = 100
    for c in cnts:
        area = cv2.contourArea(c)
        if min_area < area < max_area:        
            x,y,w,h = cv2.boundingRect(c)
            ROI = image[y:y+h, x:x+w]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 5)
    return ROI

def find_top(img,):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # BGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _ , in_range = cv2.threshold(hsv,80,255,cv2.THRESH_BINARY)
    # in_range = cv2.cvtColor(in_range, cv2.COLOR_GRAY2RGB)
    # in_range = cv2.cvtColor(in_range, cv2.COLOR_GRAY2RGB)
    new_in_range = cv2.inRange(in_range,(0,100,0),(0,255,0))
    blur = cv2.medianBlur(new_in_range, 3)

    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img_rag = cv2.inRange(hsv,(70,100,1),(90,245,60))

    cnts = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    min_area = 3000
    max_area = 6000
    check_top = 0
    for c in cnts:
        area = cv2.contourArea(c)
        # print(area)
        if min_area < area < max_area:
            # print(area)           
            x,y,w,h = cv2.boundingRect(c)
            # ROI = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 5)
            if ( x < img.shape[1] * 0.25  and y > img.shape[0] * 0.5 )or ( x > img.shape[1] * 0.75 and y < img.shape[0] * 0.5 ) :
                check_top = x
    # print(x,y,img.shape)

    if check_top < img.shape[1]/2 :
        img = imutils.rotate(img, 180)

    return img 

def find_circle(img):
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    BGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    hsv = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)
    # _ , in_range1 = cv2.threshold(hsv,73,255,cv2.THRESH_BINARY)
    _ , in_range1 = cv2.threshold(hsv,75,255,cv2.THRESH_BINARY)
    # hsv = in_range1
    # in_range = cv2.cvtColor(in_range, cv2.COLOR_GRAY2RGB)
    # in_range = cv2.cvtColor(in_range, cv2.COLOR_GRAY2RGB)
    in_range2 = cv2.inRange(in_range1,(0,0,100),(0,0,255))
    blur = cv2.medianBlur(in_range2, 5)
    # cx = 1
    # blur = cv2.blur(in_range,(cx,cx))
    # blur = cv2.GaussianBlur(in_range,(cx,cx),0)

    minDist = 25
    param1 = 25 #500
    param2 = 16 #200 #smaller value-> more false circles
    minRadius = 16
    maxRadius = 29 #10

    # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    count = 0
    Circle_data = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # circles[0] = np.uint16(np.around(sorted(circles[0], key=lambda x: x[0])))

        # row = []
        # column = [4,3,3,3,2,2,2,3,3]
        # check_count = 0
        # for i in range(9):
        #     row.append([])
        #     for j in range(column[i]):
        #         row[i].append(circles[0][check_count])
        #         check_count += 1
        #     row[i] = np.uint16(np.around(row[i]))
        #     row[i] = np.uint16(np.around(sorted(row[i], key=lambda x: x[1])))

        # circles_new = [[]]            
        # for i in range(9):
        #     for j in range(column[i]):
        #         circles_new[0].append(row[i][j])
        # circles_new = np.uint16(np.around(circles_new))

        # image_number = 0        
        for i in circles[0,:]:
        # for i in circles_new[0,:]:
            if img.shape[0]*0.13 < i[1] < img.shape[0]*0.85:
                count += 1
                x,y,_ = i
                x = x - 30
                y = y - 30
                ROI = img[y:y+60, x:x+60]
                ROI = imutils.rotate(ROI, 90)
                # ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY) # <<<<<<<<<<<<<<<<<<<<<<<<============
                # _ , ROI = cv2.threshold(ROI, 80, 255, cv2.THRESH_BINARY)

                # print(ROI)
                Circle_data.append(ROI)
                cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 5)
                # cv2.imwrite('test_save/data{}.jpg'.format(image_number), ROI)

                # cv2.putText(img, str(count) ,(x,y),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0),5)
                # image_number += 1


    return img , Circle_data , [in_range1,in_range2] , hsv



image = cv2.imread("image_Full_Menu/image_90.jpg")

img = find_square(image)
top  = find_top(img)
close , Circle_data , in_range , hsv = find_circle(top)

TARGET_SIZE = (int(1984/2),int(928/2))
# TARGET_SIZE = (992,464)

# # use in_range1 for check 25 circle
inRange1 = cv2.resize(in_range[1],TARGET_SIZE)
cv2.imshow('in_range1', inRange1)

image = cv2.resize(image,TARGET_SIZE)
cv2.imshow('image', image)

img = cv2.resize(img,TARGET_SIZE)
cv2.imshow('img', img)

hsv = cv2.resize(hsv,TARGET_SIZE)
cv2.imshow('hsv', hsv)

cv2.waitKey()