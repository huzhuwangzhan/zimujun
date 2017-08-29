from libraries import *
#from run_stt import run_stt

def read_input(INPUT_FILE):

    print 'opening input file' + INPUT_FILE

    with open(INPUT_FILE) as f:
         content = f.readlines()

    return content

def write_file(DATA,FILE,mode = "w"):

    text_file = open(FILE, mode)
    text_file.write("%s" % DATA)
    print 'writing output to file ' + FILE
    text_file.close()


def create_stt_command(INPUTFILE):

    print 'forming Julius speech 2 text shell command'

    #command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist '+ INPUTFILE + ' -demo -dnnconf julius.dnnconf $*'
    command = './bin/osx/julius -C main.jconf -C am-gmm.jconf -input rawfile -filelist '+ INPUTFILE + ' -demo $*'

    print 'shell command formed: ' + command

    return command

def run_stt(command):

    print 'Running Julius shell command'

    p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
    out, err = p.communicate()
    out_result = out[out.find('sentence1:')+11:-1]

    print 'text is subcribed'
    return out_result

#Ran successfully: jp_2_text('audio_inputs.txt','output.txt')

def jp_2_text(INPUTFILE,OUTPUTFILE):

    command = create_stt_command(INPUTFILE)
    outresult = run_stt(command)
    write_file(outresult,OUTPUTFILE)



def form_url(source,fromLang='jp',toLang='zh'):

    print 'forming url to translate: ' + source

    appid = '20170824000076401'
    secretKey = 'n0LJwTGsYSE2XBMPj0YD'
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+source+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(source)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    return myurl

def request(myurl):

    try:
        httpClient = None
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        response = httpClient.getresponse()

        return response.read().decode('unicode_escape')
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def translate(SOURCE):
    url_request = form_url(SOURCE)
    url_returned = request(url_request)
    print url_returned
    dst = url_returned[url_returned.find('"dst":') + 7:-4].encode('utf-8')
    print 'translated: '+ dst

    return dst

# Tested:  translate_fileio('trans_input_test.txt','translate_results.txt')

def translate_fileio(INPUT,OUTPUT,fromLang='jp',toLang='zh'):

    content = read_input(INPUT)
    for src in content:
        dst = translate(src)
        write_file(dst,OUTPUT,"a")

    print 'Finish translation'


# Test: jp_stt_trans_fileio('audio_inputs.txt','output.txt','translate_results.txt')

def jp_stt_trans_fileio(INPUTFILE,OUTPUTFILE,TRANSOUTPUT,fromLang='jp',toLang='zh'):

    jp_2_text(INPUTFILE,OUTPUTFILE)
    translate_fileio(OUTPUTFILE,TRANSOUTPUT,fromLang,toLang)


# Test: cut_audio('audio_5.wav', 'audio_5_test.wav',10,20)
def cut_audio(AUDIO_INPUT, AUDIO_OUTPUT,t1,t2):
    t1 = 1000*t1 #Works in milliseconds
    t2 = 1000*t2
    newAudio = AudioSegment.from_wav(AUDIO_INPUT)
    newAudio = newAudio[t1:t2]
    newAudio.export(AUDIO_OUTPUT, format="wav") #
