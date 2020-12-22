import cv2
import imutils

#  ================ rotate Original folder picture to new folder ===========================
# for i in range(1,8):
#     im = cv2.imread('Data set/Original/data set_'+str(i)+'.jpg')
#     rotated = imutils.rotate(im, 0.5)
#     cv2.imwrite('Data set/New/data'+str(i)+'.jpg',rotated)


# ============================== test code find x and y position for crop ======================================
# im = cv2.imread('Data set/New/data6.jpg')
# w = 91
# h = 91
# while(1):    
#     cv2.imshow('im',im)

    # ============================= find x y ================= eiei
    # x = 64
    # y = 77
    # crop_img0 = im[x:x+h, y:y+w]
    # cv2.imshow("cropped0", crop_img0)

    # x = x + 85
    # y = y+94
    # crop_img1 = im[x:x+h, y:y+w]
    # cv2.imshow("crop_img1", crop_img1)

    # x = x + 85
    # y = y+94
    # crop_img2 = im[x:x+h, y:y+w]
    # cv2.imshow("crop_img2", crop_img2)
    # ============================================================
    
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


# ============================ crop picture =====================================
for i in range(1,9):
    numberfile = i
    im = cv2.imread('Data set/New/data'+str(numberfile)+'.jpg')
    num = 0
    # x start 64 >> 85  , y start 77 >> 94
    w = h = 75
    x = 79
    for i in range(1,41):
    # for i in range(1,2):
        y = 88
        for j in range(1,26):
            num = num + 1
            imcrop = im[x:x+h, y:y+w]
            cv2.imwrite('Data set/New/'+str(numberfile)+'/data'+str(numberfile)+str(num)+'.jpg',imcrop)
            y = y + 96
        x = x + 85
    print("finish : ",numberfile)
print("finish All")
# ===============================================================================