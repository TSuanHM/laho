import cv2
import numpy as np


def convert(img):
	h,w = img.shape
	img = img[2:h-2,2:w-2,]
	h,w = img.shape
	img  = cv2.resize(img, (w*4,h*4))
	kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
	img = cv2.filter2D(img,-1,kernel)
	#_,img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
	return img

img = cv2.imread("D://402.jpg",0)

cv2.imwrite("D://4024.jpg",convert(img))

