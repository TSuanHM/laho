import cv2
import numpy as np
from os import walk

f = []
for (dirpath, dirnames, filenames) in walk('test2'):
    f.extend(filenames)
    break

maxw = 0
maxh = 0

imgs = []

#330 10*33

for x in f:
	img = cv2.imread("test2/"+x,0)
	h,w = img.shape
	if w > maxw:
		maxw = w
	if h > maxh:
		maxh = h
	_,img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
	imgs.append(img)

print maxh,maxw

one = np.full((maxh*33+4,maxw*10+4),255)

print one.shape

rh = 0
rw = 0

idx = 0


for row in range(1,33):
	rw = 40
	print "xxx:"+str(row)+","+str(rh)
	for row in xrange(1,10):
		h,w = imgs[idx].shape
		for j in xrange(0,h):
			for i in xrange(0,w):
				one[rh+j][rw+i] = imgs[idx][j][i]
		idx=idx+1
		rw = rw+maxw
	rh = rh+maxh

cv2.imwrite("aa.tif",one)
		



_
