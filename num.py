
from PIL import Image, ImageSequence 
import cv2 
import numpy as np
  
im = Image.open("61a2978841.gif") 

image = ImageSequence.Iterator(im)[0]

print np.array(image)

print '----------------------------'


im1 = Image.open("7290e774ee.gif") 

image1 = ImageSequence.Iterator(im1)[0]


print np.linalg.norm(np.array(image)-np.array(image1))


