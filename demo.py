# -*- coding: utf-8 -*-
import os
import cv2
import ctypes
import MySQLdb

import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect(host="192.168.181.132", user="root", passwd="root", db="gz",charset='utf8')
#c = db.cursor()
#c.execute("select * from new_house_daily")
#r = c.fetchone()
#print(r)


def insert(table,c):
	if len(c) != 12:
		return 
	else:
		sql = "insert into {0} values('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')".format(table,c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11])
		print sql
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()


#lang = "dig"
libname = "libtesseract-4.dll"
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
if not TESSDATA_PREFIX:
    TESSDATA_PREFIX = "./"

tesseract = ctypes.cdll.LoadLibrary(libname)

# tesseract.TessVersion.restype = ctypes.c_char_p
# tesseract_version = tesseract.TessVersion()
# api = tesseract.TessBaseAPICreate()
# rc = tesseract.TessBaseAPIInit3(api, TESSDATA_PREFIX, lang)
# if rc:
#     tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
#     print('Could not initialize tesseract.\n')
#     exit(3)


def from_img(img,lang='dig'):
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

zone = []

zone.append('越秀区')
zone.append('荔湾区')
zone.append('海珠区')
zone.append('天河区')
zone.append('白云区')
zone.append('黄埔区')
zone.append('番禺区')
zone.append('花都区')
zone.append('南沙区')
zone.append('萝岗区')
zone.append('从化市')
zone.append('增城市')


top = "test7/"

date = ""

for x in sorted(os.listdir(top),key=lambda k: int(k)):
	if int(x)/100 == 6:
		for _,_,filenames in os.walk(top+x):
			if len(filenames) == 1:
				fp = top+x+'/'+filenames[0]
				img = cv2.imread(fp)
				content = from_img(img,'chi_sim').replace(' ', '')
				pos = content.find('日期:')
				if pos > 0:
					pos = pos + len('日期:')
					date = content[pos:pos+10]
print date
z = 0
for x in sorted(os.listdir(top),key=lambda k: int(k)):
	if int(x) > 100 and int(x) < 600 and z < 12:
		record = []
		record.append(zone[z])
		record.append(date)
		for _,_,filenames in os.walk(top+x):
			i = 0
			for filename in sorted(filenames, key=lambda k: int(k[0:-4])):
				if i > 0:
					fp = top+x+'/'+filename
					if fp.endswith('.tif'):
						img = cv2.imread(fp)
						record.append(from_img(img).replace(' ', '').strip('\n'))
				i=i+1
		print len(record)
		insert('new_house_can_sold_daily',record)
		z=z+1
z = 0
for x in sorted(os.listdir(top),key=lambda k: int(k)):	
	if int(x) > 800 and int(x) < 1300 and z < 12:
		record = []
		record.append(zone[z])
		record.append(date)
		for _,_,filenames in os.walk(top+x):
			i = 0
			for filename in sorted(filenames, key=lambda k: int(k[0:-4])):
				if i > 0:
					fp = top+x+'/'+filename
					if fp.endswith('.tif'):
						img = cv2.imread(fp)
						record.append(from_img(img).replace(' ', '').strip('\n'))
				i=i+1
		print len(record)
		insert('new_house_not_sold_daily',record)
		z=z+1
z = 0
for x in sorted(os.listdir(top),key=lambda k: int(k)):
	if int(x) > 1450 and int(x) < 1950 and z < 12:
		record = []
		record.append(zone[z])
		record.append(date)
		for _,_,filenames in os.walk(top+x):
			i = 0
			for filename in sorted(filenames, key=lambda k: int(k[0:-4])):
				if i > 0:
					fp = top+x+'/'+filename
					if fp.endswith('.tif'):
						img = cv2.imread(fp)
						record.append(from_img(img).replace(' ', '').strip('\n'))
				i=i+1
		print len(record)
		insert('new_house_signed_daily',record)
		z=z+1
