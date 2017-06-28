import cv2


img = cv2.imread("test2/20.tif", 0)

_,bin = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)

cv2.imshow("bin",bin)
cv2.waitKey(0)