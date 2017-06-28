import cv2
import os
import ctypes
import numpy as np


# def convert(img):
# 	h,w,d = img.shape
# 	img = cv2.resize(img,(w*4,h*4))
# 	bg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# 	#kernel = [[0,-1,0],[-1,4,-1],[0,-1,0]]
# 	#kernel = np.asanyarray(kernel, np.float32)
# 	#result = cv2.filter2D(img,-1,kernel)
# 	lp = cv2.Laplacian(bg, cv2.CV_16S,3);
# 	result = cv2.convertScaleAbs(lp)
# 	#gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
# 	_,bin = cv2.threshold(bg, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
# 	bh,bw = bin.shape
# 	bin = bin[5:bh-5,5:bw-5,]
# 	return bin

def convert(img):
	bh,bw,_ = img.shape
	img = img[2:bh-2,2:bw-2,]
	h,w,d = img.shape
	img = cv2.resize(img, (w*2,h*2))
	kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
	result = cv2.filter2D(img,-1,kernel)

	#img = cv2.GaussianBlur(img, (3,3), 1.8)
	#lp = cv2.Laplacian(img,-1,7);
	#result = cv2.convertScaleAbs(lp)

	#bg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#_,bin = cv2.threshold(bg, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
	return result


def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)

#img = cv2.imread('zs.jpg')
#img = cv2.imread('gz.png')
img = cv2.imread('xsxx7.png')

h,w,_ = img.shape

#img = cv2.resize(img, (w*2, h*2))

#kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
#img = cv2.filter2D(img,-1,kernel)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h,w = gray.shape

_,bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)

scale = 20
horizontal = bin
vertical  = bin 

hs = cv2.getStructuringElement(cv2.MORPH_RECT, (int(w/scale),1))
horizontal = cv2.erode(horizontal,hs,(-1,-1))
horizontal = cv2.dilate(horizontal,hs,(-1,-1))

vs = cv2.getStructuringElement(cv2.MORPH_RECT,(1,int(h/scale)))
vertical = cv2.erode(vertical,vs,(-1,-1))
vertical = cv2.dilate(vertical,vs,(-1,-1))

mask = horizontal+vertical

joints = cv2.bitwise_and(horizontal,vertical)

i = 0
subs = []
lines = {}
contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
heirs = hierarchy[0]
for cnt, heir in zip(contours, heirs):
	 _,_,_,outer_i = heir
	 if outer_i < 0:
	 	continue
	 poly = cv2.approxPolyDP(cnt,3,True)
	 r = cv2.boundingRect(poly)
	 sub = img[r[1]:r[1]+r[3],r[0]:r[0]+r[2],]
	 if lines.get(r[1]) is None:
	 	lines[r[1]] = [(r[0],sub)]
	 else:
	 	lines[r[1]].append((r[0],sub))
	 name = "/Users/huiming/Downloads/ocr/test/" + str(i) + ".jpg"
	 #cv2.imwrite(name,sub)
	 #if i == 0:
	 #	img = convert(sub)
	 #	cv2.imshow("0",img)
	 #	cv2.imwrite("00.jpg", img)
	 #	print from_img(img)
	 i=i+1

print len(lines)

path = "test7/"
create_dir(path)
for k,v in lines.items():
	newpath = path + "/" + str(k)
	create_dir(newpath)
	for p in v:
		pos,sub = p
		name = newpath + "/" + str(pos) + ".tif"
		cv2.imwrite(name, convert(sub))


#cv2.imshow('joint', joints)
#cv2.imshow('img',img)
#cv2.waitKey(0)