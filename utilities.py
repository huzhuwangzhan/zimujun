import httplib
import md5
import urllib
import random
import subprocess
from pydub import AudioSegment
import os
import time
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import glob
import re
import soundfile as sf
import sounddevice as sd
import pyautogui

def read_input(INPUT_FILE):

    print('opening input file' + INPUT_FILE)

    with open(INPUT_FILE) as f:
         content = f.readlines()

    return content

def write_file(DATA,FILE,mode = "w"):

    text_file = open(FILE, mode)
    text_file.write("%s" % DATA)
    print('writing output to file ' + FILE)
    text_file.close()


def create_stt_command(INPUTFILE):

    print('forming Julius speech 2 text shell command')

    #command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist '+ INPUTFILE + ' -demo -dnnconf julius.dnnconf $*'
    command = './bin/osx/julius -C main.jconf -C am-gmm.jconf -input rawfile -filelist '+ INPUTFILE + ' -demo $*'

    print('shell command formed: ' + command)

    return command

def run_stt(command):

    print('Running Julius shell command')

    p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
    out, err = p.communicate()
    out_result = out[out.find('sentence1:')+11:-1]

    print('text is subcribed')
    return out_result

#Ran successfully: jp_2_text('audio_inputs.txt','output.txt')

def jp_2_text(INPUTFILE,OUTPUTFILE):

    command = create_stt_command(INPUTFILE)
    outresult = run_stt(command)
    write_file(outresult,OUTPUTFILE)



def form_url(source,fromLang='jp',toLang='zh'):

    print('forming url to translate: ' + source)

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
    except e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

def translate(SOURCE):
    url_request = form_url(SOURCE)
    url_returned = request(url_request)
    print(url_returned)
    dst = url_returned[url_returned.find('"dst":') + 7:-4].encode('utf-8')
    print('translated: '+ dst)

    return dst

# Tested:  translate_fileio('trans_input_test.txt','translate_results.txt')

def translate_fileio(INPUT,OUTPUT,fromLang='jp',toLang='zh'):

    content = read_input(INPUT)
    for src in content:
        dst = translate(src)
        write_file(dst,OUTPUT,"a")

    print('Finish translation')


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

#

'''Only used by splitAudio. Modified from pydub.slience.split_on_slience'''
def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-16, keep_silence=100):
    """
    audio_segment - original pydub.AudioSegment() object
    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms
    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS
    keep_silence - (in ms) amount of silence to leave at the beginning
        and end of the chunks. Keeps the sound from sounding like it is
        abruptly cut off. (default: 100ms)
    """

    not_silence_ranges = detect_nonsilent(audio_segment, min_silence_len, silence_thresh)

    chunks = []
    for start_i, end_i in not_silence_ranges:
        start_i = max(0, start_i - keep_silence)
        end_i += keep_silence

        chunks.append(audio_segment[start_i:end_i])

    return chunks, not_silence_ranges

# splitAudio("Chinese_story_wav.wav","./")
def splitAudio(INPUT_AUDIOFILE,OUTPUT_SPLITAUDIO_LOC,min_silence_len=500,silence_thresh=-40,keep_silence=3000):
    if not os.path.isfile(INPUT_AUDIOFILE):
        print(INPUT_AUDIOFILE, " not found!")
        return None
    sound_file = AudioSegment.from_wav(INPUT_AUDIOFILE)
    audio_chunks, not_silence_ranges = split_on_silence(sound_file, min_silence_len,silence_thresh,keep_silence)

    if "/" in INPUT_AUDIOFILE:
        INPUT_AUDIOFILE = INPUT_AUDIOFILE.split('/')[-1]
    OUTPUT_targetfolder = OUTPUT_SPLITAUDIO_LOC + "/split_" + INPUT_AUDIOFILE + "_" + time.strftime("%Y_%m_%d_%H_%M_%S")
    for i, chunk in enumerate(audio_chunks):
        if not os.path.exists(OUTPUT_targetfolder):
            os.mkdir(OUTPUT_targetfolder)
        out_file = OUTPUT_targetfolder+"/chunk{0}.wav".format(i)
        print("exporting", out_file)
        chunk.export(out_file, format="wav")
    print("Successfully splitted ", INPUT_AUDIOFILE, " to ", OUTPUT_SPLITAUDIO_LOC)
    return OUTPUT_targetfolder,not_silence_ranges


# audio_2_text('split_Chinese_story_wav.wav_2017_09_23_21_18_35/','dictation_output.txt')
def audio_2_text(AUDIO_DIR,TEXT_FILE):

    i=0
    for file in glob.glob(AUDIO_DIR+"*.wav"):
        i += 1
        TEMP_FILE = AUDIO_DIR+str(i)+TEXT_FILE
        if not os.path.isfile(TEMP_FILE):
            f = open(TEMP_FILE, 'w')
            f.close()

        data, samplerate = sf.read(file) #data in bit,  hence len(data)/samplerate = [s]
        sd.play(data,samplerate,device=3)

        command = 'open -a TextEdit '+TEMP_FILE
        p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
        time.sleep(3)
        pyautogui.press(['fn','fn'])
        time.sleep(len(data)/samplerate+5)
        pyautogui.press(['fn', 'fn'])
        time.sleep(2)
        print("...Dictation service should be closed already now")
        time.sleep(2)


        command = 'pgrep TextEdit'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        pid = int(str(p.stdout.readlines())[3:-4])
        command = 'osascript -e \' tell application "TextEdit" to quit\' '
        # 'killall TextEdit'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        print("...TextEdit should be closed already now")


    files = glob.glob(AUDIO_DIR+"*.txt")
    files.sort(key=os.path.getmtime)
    concat = ','.join([open(f).read() for f in files])

    pattern = re.compile(r'(,\s){2,}')
    concat = re.sub(pattern,',',concat)

    text_file = open(AUDIO_DIR+'all.txt', 'w')
    text_file.write("%s" % concat)
    print('writing output to file ' + concat)
    text_file.close()

    os.chdir(AUDIO_DIR)
    os.system("sed 's/,\{2,\}/,/g' all.txt > final_all.txt")

def main():
    INPUT_AUDIOFILE = "Chinese_story_wav.wav"
    OUTPUT_SPLITAUDIO_LOC = "./"
    OUTPUT_targetfolder, not_silence_ranges= splitAudio(INPUT_AUDIOFILE, OUTPUT_SPLITAUDIO_LOC, min_silence_len=500, silence_thresh=-40, keep_silence=3000)
    print("OUTPUT_SPLITAUDIO_LOC",OUTPUT_targetfolder)
    audio_2_text(OUTPUT_targetfolder+'/','dictation_output.txt')
    # audio_2_text('split_Chinese_story_wav.wav_2017_09_23_21_18_35/', 'dictation_output.txt')

if __name__ == '__main__':
    main()

