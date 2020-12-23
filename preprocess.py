import cv2
import numpy as np
import imutils

def FindMenuImageContours(im):
    low = 0
    high = 80
    img = cv2.inRange(im,(low,low,low),(high,high,high))

    Mask = cv2.medianBlur(img,3)
    kernel = np.ones((9,9),np.uint8)
    Im_erode = cv2.erode(Mask,kernel,iterations = 1)

    contours, _  = cv2.findContours(Im_erode,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:    
        if( 7000000 > cv2.contourArea(cnt) > 6000000):
            approx = cv2.approxPolyDP(cnt, 0.005 * cv2.arcLength(cnt, True), True)
            # image = cv2.drawContours(im, [approx], 0, (0,0,255), 5)
            # if draw :
            #     cv2.drawContours(im, [approx], 0, (0,0,255), 5)
            n = approx.ravel()  
            # print(cv2.contourArea(cnt))    

    return n 

def line_equation(y,x1,y1,x2,y2):
    x = ( ( ( y - y1 ) * ( x2 - x1 ) ) / ( y2 - y1 ) ) + x1
    return x

def Find_angle(a,c):
    # a is Line opposite the corner  and  c is Top border of image
    return np.arctan(a/c)/np.pi*180

def Find_XY(n):
    N = [n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[7]]
    n_check = [n[0]*n[1],n[2]*n[3],n[4]*n[5],n[6]*n[7]]        
    # print(N)
    # print(n_check)
    # print(min(n_check))
    # print(n_check.index(min(n_check)))

    x1 = N[((n_check.index(min(n_check)) +1 ) * 2) - 1]
    y1 = N[((n_check.index(min(n_check)) +1 ) * 2) - 2]

    N.pop( ((n_check.index(min(n_check)) +1 ) * 2) -1)
    N.pop( ((n_check.index(min(n_check)) +1 ) * 2) -2)
    n_check.pop(n_check.index(min(n_check)))

    x2 = N[((n_check.index(min(n_check)) +1 ) * 2) - 1]
    y2 = N[((n_check.index(min(n_check)) +1 ) * 2) - 2]

    N.pop( ((n_check.index(min(n_check)) +1 ) * 2) -1)
    N.pop( ((n_check.index(min(n_check)) +1 ) * 2) -2)
    n_check.pop(n_check.index(min(n_check)))

    # print(N)
    # Menu_Width = 0
    # Menu_Length = 0

    # print(N)
    # print(n_check)
    # print(min(n_check))
    # print(y1,x1,y2,x2)
    # print("-*-")
    # print(N)

    x4 = N[((n_check.index(min(n_check)) +1 ) * 2) - 1]

    Width = np.abs( x4 - x1)
    Length = np.abs( y2 - y1 )

    return x1 , y1 , x2 , y2 , Width , Length

def Find_Degree(im):
    degree = 0
     
    n = FindMenuImageContours(im)
    # find (x1,y1) and (x2,y2)
    x1 , y1 , x2 , y2 , _ , _= Find_XY(n)
    c = im.shape[1]


    if n[6] < n[2]:
        # ------------
        # ---------
        # -----
        # --

        # y = 0
        a = line_equation(0,x1,y1,x2,y2)
        check = line_equation(im.shape[1],x1,y1,x2,y2)
        if check > 0 :
            a = a - check
        degree = Find_angle(a,c) * -1
        
    else :
        # ------------
        # ...---------
        # ......------
        # .........---

        # y = ขอบรูป
        a = line_equation(im.shape[1],x1,y1,x2,y2)
        check = line_equation(0,x1,y1,x2,y2)
        if check > 0 :
            a = a - check
        degree = Find_angle(a,c)
    return degree

def Find_Circle(Menu):
    # Menu have 36 circle
    circle = []

    # Step0 have 3 circle    
    XY = [[75,500],[42,732],[105,732]]
    for i in range(3):
        x , y = XY[i]
        circle.append(Menu[ x : x + 60 ,y : y + 60 ].tolist())
    
    

    # Step1 have 4 circle
    Y = [ 133 , 330 , 532 , 725 ]
    for i in range( 4 ):
        x , y = 320 , Y[i]
        circle.append(Menu[ x : x + 60 ,y : y + 60 ].tolist())

    # # Step2 have 9 circle
    X = [ 680 , 785 , 895 ]
    Y = [ 65 , 380 , 633 ]
    for i in range(3):        
        for j in range(3):    
            x , y = X[i] , Y[j]
            circle.append(Menu[ x : x + 60 ,y : y + 60 ].tolist())

    # Step3 have 6 circle
    X = [ 1207 , 1297 ]
    Y = [ 110 , 325 , 580 ]
    for i in range(2):        
        for j in range(3):    
            x , y = X[i] , Y[j]
            circle.append(Menu[ x : x + 60 ,y : y + 60 ].tolist())

    # Step4 have 9 circle
    X = [ 1485 , 1560 , 1645]
    Y = [ 116 , 320 , 537 ]
    for i in range(3):        
        for j in range(3):    
            x , y = X[i] , Y[j]
            circle.append(Menu[ x : x + 60 ,y : y + 60 ].tolist())

    # Step5 have 5 circle
    Y = [ 66 , 245 , 430 , 615 , 792]
    for i in range( 5 ):
        x , y = 1843 , Y[i]
        circle.append(Menu[ x : x + 60 ,y : y + 60 ].tolist())

    circle = np.array(circle).astype(np.uint8)
    return circle

def preprocess(im):
    # im = cv2.imread("image_Full_Menu/image_99.jpg")

    # Straighten the picture (ปรับองศาของรูปภาพให้ตรง)
    im = imutils.rotate(im, Find_Degree(im))

    # find Width , Length
    n = FindMenuImageContours(im)
    x , y , _ , _ , Menu_Width , Menu_Length = Find_XY(n)

    # crop image
    Menu = im[ x : x + Menu_Width ,y : y + Menu_Length ]

    # Fixed the size  (ปรับขนาดของภาพให้คงที่)
    # Menu = cv2.resize(Menu,(1344,1512))
    Menu = cv2.resize(Menu,(920,1980))
    # cv2.imshow('Menu',Menu)

    # find Circle on image (หาจำนวนวงกลมทั้งหมดที่มีในรูปภาพ โดยทำการเร็งเฉพาะตามตำแหน่งที่ได้ตั้งค่าไว้)
    Circle = Find_Circle(Menu)
    # print(len(Circle))
    # !!!!!!!!!!!!!!!!!!!!!!! แค่จะโชว์ออกมาดูเฉยๆๆๆๆๆ ไม่มีความสำคัญเลยจ้าาาาาาา !!!!!!!!!!!!!!!!!!!!!!!!
    # for i in range(31,36):
    #     cv2.imshow('Circle'+str(i),Circle[i])

    # size = 1.2
    # TARGET_SIZE = (int(Menu.shape[0]/(3.5*size)),int(Menu.shape[1]/size))
    # image = cv2.resize(Menu,TARGET_SIZE)
    # cv2.imshow('image',image)

    return Circle
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
