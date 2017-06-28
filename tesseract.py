import ctypes 
import cv2
import os
import os.path
import numpy as np


lang = "dig+chi_sim"
filename = "test2/208.tif"
libname = "libtesseract-4.dll"
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
if not TESSDATA_PREFIX:
    TESSDATA_PREFIX = "./"

# tesseract = ctypes.cdll.LoadLibrary(libname)
# tesseract.TessBaseAPICreate.restype = ctypes.c_uint64
# api = tesseract.TessBaseAPICreate()
# rc = tesseract.TessBaseAPIInit3(ctypes.c_uint64(api), TESSDATA_PREFIX, lang)
# #b = tesseract.TessBaseAPISetVariable(api,b'tessedit_char_whitelist', b'0123456789');
# print rc

tesseract = ctypes.cdll.LoadLibrary(libname)
tesseract.TessVersion.restype = ctypes.c_char_p
tesseract_version = tesseract.TessVersion()
api = tesseract.TessBaseAPICreate()
rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
if rc:
    tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
    print('Could not initialize tesseract.\n')
    exit(3)

def from_img(img):
    api = tesseract.TessBaseAPICreate()
    rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
    if rc:
        tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
        print('Could not initialize tesseract.\n')
        exit(3)
    h,w,d= img.shape
    tesseract.TessBaseAPISetImage.restype = None
    tesseract.TessBaseAPISetImage.argtypes = (
            ctypes.c_long, # handle
            ctypes.c_void_p, # imagedata
            ctypes.c_int,    # width
            ctypes.c_int,    # height
            ctypes.c_int,    # bytes_per_pixel
            ctypes.c_int)

    tesseract.TessBaseAPISetPageSegMode.restype = None
    tesseract.TessBaseAPISetPageSegMode.argtypes = (
            ctypes.c_long,
            ctypes.c_int)

    tesseract.TessBaseAPISetVariable.restype = ctypes.c_bool
    tesseract.TessBaseAPISetVariable.argtypes = (
        ctypes.c_ulong,
        ctypes.c_char_p,
        ctypes.c_char_p
        )


    #tesseract.TessBaseAPISetPageSegMode(api,3)

    tesseract.TessBaseAPISetImage(api, img.ctypes, w, h, d, w*d)
    tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
    text_out = tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(api))
    result =  ctypes.string_at(text_out)
    tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
    return result
    pass

def from_file(path):
    im = cv2.imread(path)
    result = line_split(im)
    h,w = result[1].shape
    t = result[1]
    print from_img(t)
    gray = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,3))
    dst = cv2.erode(gray,kernel,(1,1),iterations=1)
    cv2.imshow("ddd", dst)
    # i = 0
    # for r in result:
    #     cv2.imshow(str(i), r)
    #     print from_img(r)
    #     i = i+1
    #     pass
    cv2.waitKey(0)


def line_split(img):
    lines = []
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize = 3)
    _,bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 3))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 3))
    dilation = cv2.dilate(bin, element2, iterations = 1)
    erosion = cv2.erode(dilation, element1, iterations = 1)
    dilation2 = cv2.dilate(erosion, element2, iterations = 3)
    contours,hierarchy = cv2.findContours(dilation2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        r = cv2.boundingRect(cnt)
        sub = bin[r[1]:r[1]+r[3],r[0]:r[0]+r[2],]
        lines.append(sub)
        pass

    cv2.imshow("img", lines[0])
    #col
    l0 = lines[0]
    e1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 20))
    e2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 30))
    d1 = cv2.dilate(l0, e2, iterations = 1)
    er0 = cv2.erode(d1, e1, iterations = 1)
    d2 = cv2.dilate(er0,e2, iterations = 3)

    cv2.imshow("lo", d2)
    cv2.waitKey()

def col_split(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    e1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 20))
    e2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 30))
    d1 = cv2.dilate(bin, e2, iterations = 1)
    er0 = cv2.erode(d1, e1, iterations = 1)
    d2 = cv2.dilate(er0,e2, iterations = 3)

    contours,hierarchy = cv2.findContours(d1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    v = []
    for cnt in contours:
        r = cv2.boundingRect(cnt)
        if np.float(r[3])/r[2] > 1.5:
            continue
        sub = img[r[1]:r[1]+r[3],r[0]:r[0]+r[2],]
        sub = cv2.copyMakeBorder(sub, 0, 0, 3, 3, cv2.BORDER_CONSTANT)
        path = "/Users/huiming/Downloads/ocr/single/" + str(i) + ".jpg"
        cv2.imwrite(path, sub)
        v.append(from_img(sub))
        cv2.rectangle(img, (r[0],r[1]), (r[0]+r[2],r[1]+r[3]), (255,0,255))
        i=i+1
    print '-----------------------------------------------'
    for x in v:
        print x
        pass

    #cv2.imshow("winname", d2)
    #cv2.imshow("img", img)
    #cv2.waitKey(0)

# if __name__ == '__main__':
#     image_file_path = b'./00.jpg'
#     img = cv2.imread(image_file_path)
#     print from_img(img)


def single_line(img):

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,bin = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    e1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
    e2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
    d1 = cv2.dilate(bin, e2, iterations = 1)
    er0 = cv2.erode(d1, e1, iterations = 1)
    d2 = cv2.dilate(er0,e2, iterations = 3)
    contours,hierarchy = cv2.findContours(d1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    boxs = [cv2.boundingRect(c) for c in contours]
    boxs.sort(key=lambda x:x[0])
    for box in boxs:
        x,y,w,h = box
        sub = img[y:y+h,x:x+w,]
        sub = cv2.copyMakeBorder(sub, 5, 5, 10, 10, cv2.BORDER_CONSTANT)
        print "value:" + from_img(sub)
        path = "/Users/huiming/Downloads/ocr/temp/" + str(x) + ".jpg"
        cv2.imwrite(path, sub)
        cv2.rectangle(img, (x,y),(x+w,y+h), (255,0,255))
        pass
    cv2.imshow("winname", img)
    cv2.waitKey(0)

f1 = open('result.txt','w')

if __name__ == '__main__':
    result = {}
    top = "test2/"
    #top = "/Users/huiming/Downloads/ocr/temp/"
    for _,_,filenames in os.walk(top):
        for filename in filenames:
            if filename.endswith('.tif'):
                file = top + filename
                img = cv2.imread(file)
                result[filename] = from_img(img)
                #print filename, result[filename]
                f1.write(filename)
                f1.write(",")
                f1.write(result[filename])

    print '-------------------------------------'
    f1.close()
    for k,v in result.items():
        print k,':',v

    #single_line(cv2.imread("test3/123/276.jpg"))

















