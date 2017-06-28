# -*- coding: utf-8 -*-

import urllib2
import chardet
import random
import bs4
from bs4 import BeautifulSoup
import MySQLdb
import re

from PIL import Image, ImageSequence 
import cv2 
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

db = MySQLdb.connect(host="192.168.181.132", user="root", passwd="root", db="gz",charset='utf8')
#c = db.cursor()
#c.execute("select * from new_house_daily")
#r = c.fetchone()
#print(r)


def insert(table,c):
  if len(c) != 8:
    return 
  else:
    sql = "insert into {0} values('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(table,c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7])
    print sql
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


   


hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

digital_dict = [
'79a0dfff47',
'96a5dbc554',
'453e9b408a',
'e7e7e3f727',
'03335dba0d',
'61a2978841',
'23f3507e64',
'c9645a9a2b',
'e0524a8781',
'44dfae52d5'
]

digital_vec = []

def get_image_label(url):
  im = get_image_vec(url)
  min = float('+inf')
  label = 0
  i  = 0
  for x in digital_vec:
    v = np.linalg.norm(im-x)
    if min >= v:
      min = v
      label = i
    i = i+1
  return label




def get_image_vec(url):

  try:
    req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
    data = urllib2.urlopen(req,timeout=10)
    im = Image.open(data)
    return np.array(ImageSequence.Iterator(im)[0])
  except (urllib2.HTTPError, urllib2.URLError), e:
    print e
    exit(-1)
  except Exception,e:
     print e
     exit(-1)


def init_num_rec():
  for d in digital_dict:
    path = "../color_digital/" + d + ".gif"
    im = Image.open(path) 
    image = ImageSequence.Iterator(im)[0]
    digital_vec.append(np.array(image))


  
def do_page(page = 0):
  u = ""
  if page == 0:
    u = "http://housing.gzcc.gov.cn/fyxx/ysz/index.shtml"
  else:
    u = "http://housing.gzcc.gov.cn/fyxx/ysz/index_{0}.shtml".format(page)
  try:
    req = urllib2.Request(u,headers=hds[random.randint(0,len(hds)-1)])
    source_code = urllib2.urlopen(req,timeout=10).read()
    #print(chardet.detect(source_code))
    #plain_text=unicode(source_code, 'GB2312')#,errors='ignore') 
    soup = BeautifulSoup(source_code)
    plist = soup.findAll('table',{'class':'box_tab_style02 lh24 mt10'})[0].findAll('tr')
    for tr in plist:
      row = []
      url = ""
      for td in tr.findAll('td'):
        row.append(td.get_text())
        for link in td.find_all('a'):
          url = link.get('href')
      row.append(url)
      insert('new_house_prepare_sell',row[1:])


  except (urllib2.HTTPError, urllib2.URLError), e:
    print e
    exit(-1)
  except Exception,e:
     print e
     exit(-1)

def get_info_url(url):
  url_list = []
  u = 'http://housing.gzcc.gov.cn/'+url
  try:
    pattern = re.compile(r'url="(.*?)"')
    req = urllib2.Request(u,headers=hds[random.randint(0,len(hds)-1)])
    source_code = urllib2.urlopen(req,timeout=10).read()
    #print(chardet.detect(source_code))
    #plain_text=unicode(source_code, 'GB2312')#,errors='ignore')
    #print plain_text
    match = pattern.findall(source_code)
    for x in match:
      if len(x) > 0:
        url_list.append(x)
    return url_list
  except (urllib2.HTTPError, urllib2.URLError), e:
    print e
    #exit(-1)
  except Exception,e:
    print e
    #exit(-1)


ddict = {}

def info(url):
  ulist = get_info_url(url)
  if len(ulist) < 1:
    return None
  try:
    req = urllib2.Request('http://housing.gzcc.gov.cn/search/project/'+ulist[0],headers=hds[random.randint(0,len(hds)-1)])
    source_code = urllib2.urlopen(req,timeout=10).read()
    #print(chardet.detect(source_code))
    #plain_text=unicode(source_code, 'GB2312')#,errors='ignore')
    soup = BeautifulSoup(source_code)
    plist = soup.findAll('table')
    vv = []
    for tr in plist[0].findAll('tr'):
        i = 1
        for td in tr.findAll('td'):
          if i%2 == 0 :
            content = ''
            for c in td.contents:
              if isinstance(c, bs4.element.NavigableString):
                content += c.string
              else: 
                if isinstance(c,bs4.element.Tag):
                  if len(c.attrs) > 0:
                    key = c.attrs['src'][8:-4]
                    if ddict.get('key') != None:
                      content+=ddict[key]
                    else:
                      url = "http://housing.gzcc.gov.cn/"+c.attrs['src']
                      ddict[key] = str(get_image_label(url))
                      content+=ddict[key]
            vv.append(content)
          i=i+1
    sql = "insert ignore into new_house_base_info values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}',\
            '{9}','{10}','{11}','{12}','{13}','{14}')".format(vv[1],vv[0],vv[2],vv[3],vv[4],vv[5],vv[6],vv[7],vv[8],vv[9],vv[10],vv[11],vv[12],vv[13],vv[14])
    print sql
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

  except (urllib2.HTTPError, urllib2.URLError), e:
    print e
  except Exception,e:
    print e

def get_pre_sell_url():
  cursor = db.cursor()
  cursor.execute('select url from new_house_prepare_sell where id > 20170372');
  results = cursor.fetchall()
  for url in results:
    print url[0]
    info(url[0])


if __name__ == '__main__':
  init_num_rec()
  get_pre_sell_url();
  #print get_image_label('http://housing.gzcc.gov.cn//images/6f798f29ba.gif')
  #for i in range(0,312):
    #do_base_info("")
