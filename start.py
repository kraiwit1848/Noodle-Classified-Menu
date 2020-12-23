import cv2
import numpy as np
# import imutils
# from keras.models import Model, load_model

from preprocess import preprocess

im = cv2.imread("image_Full_Menu/image_99.jpg")
test = preprocess(im)
print(len(test))

# !!!!!!!!!!!!!!!!!!!!!!! แค่จะโชว์ออกมาดูเฉยๆๆๆๆๆ ไม่มีความสำคัญเลยจ้าาาาาาา !!!!!!!!!!!!!!!!!!!!!!!!
for i in range(31,36):
    cv2.imshow('Circle'+str(i),test[i])
cv2.waitKey(0)
cv2.destroyAllWindows()
# /////////////////////////////////////////////////////////////////////////////

