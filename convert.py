import cv2
import numpy as np


def  thin(img):
	w,h = img.shape
	Zhangmude = np.zeros((9,),np.int32)
	deletelist1 = []
	while True:
		for j in xrange(1,w-1):
			data_last = img[j-1]
			data = img[j]
			data_next = img[j+1]
			for i in xrange(1,h-1):
				if (data[i] == 255):
					Zhangmude[0]=1;
					if (data_last[i]==255):
						Zhangmude[1]=1
					else:
						Zhangmude[1]=0
					if (data_last[i+1]==255):
						Zhangmude[2]=1
					else:
						Zhangmude[2]=0
					if (data[i+1]==255):
						Zhangmude[3]=1
					else:
						Zhangmude[3]=0
					if (data_next[i+1]==255):
						Zhangmude[4]=1
					else:
						Zhangmude[4]=0
					if (data_next[i]==255):
						Zhangmude[5]=1
					else:
						Zhangmude[5]=0
					if (data_next[i-1]==255):
						Zhangmude[6]=1
					else:
						Zhangmude[6]=0
					if (data[i-1]==255):
						Zhangmude[7]=1
					else:
						Zhangmude[7]=0
					if (data_last[i-1]==255):
						Zhangmude[8]=1
					else:
						Zhangmude[8]=0
					wptotoal = 0
					for x in xrange(1,9):
						wptotoal = wptotoal+Zhangmude[k]
						pass

					if (wptotoal >=2) and (wptotoal<=6):
						ap = 0
						if(Zhangmude[1]==0) and (Zhangmude[2]==1):
							ap = ap+1
						if (Zhangmude[2]==0) and (Zhangmude[3]==1):
							ap = ap+1
						if (Zhangmude[3]==0) and (Zhangmude[4]==1):
							ap = ap+1
						if (Zhangmude[4]==0) and (Zhangmude[5]==1):
							ap = ap+1
						if (Zhangmude[5]==0) and (Zhangmude[6]==1):
							ap = ap+1
						if (Zhangmude[6]==0) and (Zhangmude[7]==1):
							ap = ap+1
						if (Zhangmude[7]==0) and (Zhangmude[8]==1):
							ap = ap+1
						if (ap==1):
							if (Zhangmude[1]*Zhangmude[7]*Zhangmude[5]==0) and (Zhangmude[3]*Zhangmude[5]*Zhangmude[7]==0):
								deletelist1.append((i,j))
				pass
			pass
		pass
		if len(deletelist1) == 0:
			break
		for p in deletelist1:
			(x,y) = p
			img[y][x] = 0
			pass
		deletelist1 = []
	pass



def strength(img):
	his = np.zeros((256,))
	p_hist = np.zeros((256,))
	s_hist = np.zeros((256,))
	h,w,_=img.shape
	print w,h
	total = w*h
	for i in xrange(0,h):
		for j in xrange(0,w):
			his[img[i][j]] = his[img[i][j]]+1
			pass
		pass
	for i in xrange(0,256):
		p_hist[i]=his[i]/total;
		if (i==0):
			s_hist[i]=p_hist[i]
		else:
			s_hist[i]=s_hist[i-1]+p_hist[i]
		pass
	for i in xrange(0,h):
		for j in xrange(0,w):
			img[i][j] = np.uint8(s_hist[img[i][j]]*255+0.5)
			pass
		pass


def trunc(img):
	h,w=img.shape
	for j in xrange(0,h):
		for i in xrange(0,w):
			if (img[j][i] < 180):
				img[j][i] = 0
			else:
				img[j][i] = 255
			pass
		pass

img = cv2.imread('../132.jpg')
h,w,d = img.shape
img = cv2.resize(img,(w*2,h*2))
bg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('img',img)
#c = cv2.Canny(bg,33,20)
# strength(img)
#cv2.imshow("canny",c)
#cv2.waitKey(0)

kernel = [[0,-1,0],[-1,5,-1],[0,-1,0]]
kernel = np.asanyarray(kernel, np.float32)
result = cv2.filter2D(img,-1,kernel)
gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
print gray
#trunc(gray)
cv2.imshow('sss',gray)



# kernel2 = np.ones((3,3),np.float32)
# result = cv2.filter2D(result,-1,kernel2)

#element1 = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
#element2 = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))

#r1 = cv2.erode(result,element1);
# r2 = cv2.dilate(r1, element2)
#cv2.imshow('r1',r1)

#gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
# lap = cv2.Laplacian(gray,cv2.CV_16S) 
# dst = cv2.convertScaleAbs(lap)
# cv2.imshow('lap',dst);
#bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,35,50)
#blur = cv2.GaussianBlur(gray,(3,3),0)  
_,bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)

cv2.imshow('bin',bin)
cv2.imwrite('../132_.jpg',bin)
cv2.waitKey(0)