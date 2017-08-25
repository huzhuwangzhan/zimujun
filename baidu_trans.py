import httplib
import md5
import urllib
import random
from global_vars import *



def form_url(q,fromLang='en',toLang='zh'):

    appid = '20170824000076401'
    secretKey = 'n0LJwTGsYSE2XBMPj0YD'


    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()

    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    return myurl

def request(myurl):

    try:
        httpClient = None
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        response = httpClient.getresponse()

        print response.read().decode('unicode_escape')
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def read_input(INPUT_FILE):
    with open(INPUT_FILE) as f:
         content = f.readlines()
    return content

def main():

    fromLang='en'
    toLang='zh'

    content = read_input(INPUT_FILE)
    for src in content:
        myurl = form_url(src,fromLang,toLang)
        request(myurl)


if __name__ == '__main__':
    main()