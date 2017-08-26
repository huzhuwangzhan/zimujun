#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import random
from baidu_api import *

def read_input(filename):
    # q = 'apple'
    # q = raw_input('Input the word you want to search:')
    with open(filename) as f:
        content = f.readlines()
    return content

def form_url(q,fromLang='en',toLang='zh'):
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    return myurl

def trans_baidu(myurl):
    try:
        httpClient = None
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        #response是HTTPResponse对象
        response = httpClient.getresponse()
        # print(response.read().decode('unicode-escape'))
        return response.read().decode('unicode-escape')

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def main():

    fromLang = 'jp'
    toLang = 'zh'


    q = read_input('trans_input_test.txt')
    for src in q:
        myurl = form_url(src,fromLang,toLang)
        out_baidu = trans_baidu(myurl)
        out_baidu_dst = out_baidu[out_baidu.find('"dst":')+7:-4]
        out_trans = out_baidu_dst.encode('utf8')
        # print out_trans
        text_file = open("trans_output_test.txt", "w")
        text_file.write("%s" % out_trans)
        text_file.close()


if __name__ == '__main__':
    main()