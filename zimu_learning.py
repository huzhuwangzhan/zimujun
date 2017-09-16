####################################
#region Cut audio
from pydub import AudioSegment
    t1 = 1000 #Works in milliseconds
    t2 = 1000*10
    newAudio = AudioSegment.from_wav("audio_5.wav")
    newAudio = newAudio[t1:t2]
    newAudio.export('audio_5_10s.wav', format="wav") #
#endregion

#region Method 1: one single wav file to text file using mac dictation by calling Audacity
import subprocess
import pyautogui
import time
import os
import soundfile as sf
import sounddevice as sd
INPUT_AUDIOFILE = 'audio_5_10s.wav'
INPUT_FILE = 'helloworld.txt'
if not os.path.isfile(INPUT_FILE):
    f = open(INPUT_FILE,'w')
    f.close()
command = 'open -a Audacity '+INPUT_AUDIOFILE
p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
time.sleep(3)
pyautogui.hotkey('shift','space')
command = 'open -a TextEdit '+INPUT_FILE
p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
time.sleep(3)
pyautogui.press(['fn','fn'])
#endregion

#region Method 2: one single wav file to text file using mac dictation by sounddevice package
import subprocess
import pyautogui
import time
import os
import soundfile as sf
import sounddevice as sd
INPUT_AUDIOFILE = 'Chinese_story_wav.wav'
INPUT_FILE = 'helloworld.txt'
if not os.path.isfile(INPUT_FILE):
    f = open(INPUT_FILE,'w')
    f.close()
data, samplerate = sf.read(INPUT_AUDIOFILE) #data in bit,  hence len(data)/samplerate = [s]
sd.query_devices()
sd.play(data,samplerate,device=3)
command = 'open -a TextEdit '+INPUT_FILE
p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
time.sleep(3)
pyautogui.press(['fn','fn'])
#endregion

#region break sound wave based on quietness
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent

sound_file = AudioSegment.from_wav(INPUT_AUDIOFILE)
print('average loudness of the sound is ', sound_file.dBFS)
audio_chunks, not_silence_ranges = split_on_silence(sound_file,min_silence_len=500,silence_thresh=-40,keep_silence=3000)

for i, chunk in enumerate(audio_chunks):
    if not os.path.exists("./splitAudio/"):
        os.mkdir("./splitAudio/")
    out_file = ".//splitAudio//chunk{0}.wav".format(i)
    print("exporting", out_file)
    chunk.export(out_file, format="wav")
#endregion

#region speech to subspeech to subtext to text pipeline
import subprocess
import pyautogui
import time
import os
import soundfile as sf
import sounddevice as sd
import glob
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import psutil


def processExists(processname):
    '''Windows only '''
    tlcall = 'TASKLIST', '/FI', 'imagename eq %s' % processname
    # shell=True hides the shell window, stdout to PIPE enables
    # communicate() to get the tasklist command result
    tlproc = subprocess.Popen(tlcall, shell=True, stdout=subprocess.PIPE)
    # trimming it to the actual lines with information
    tlout = tlproc.communicate()[0].strip().split('\r\n')
    # if TASKLIST returns single line without processname: it's not running
    if len(tlout) > 1 and processname in tlout[-1]:
        print('process "%s" is running!' % processname)
        return True
    else:
        print(tlout[0])
        print('process "%s" is NOT running!' % processname)
        return False

INPUT_AUDIOFILE = 'Chinese_story_wav.wav'
sound_file = AudioSegment.from_wav(INPUT_AUDIOFILE)
# print('average loudness of the sound is ', sound_file.dBFS)
audio_chunks, not_silence_ranges = split_on_silence(sound_file,min_silence_len=500,silence_thresh=-40,keep_silence=3000)
for i, chunk in enumerate(audio_chunks):
    if not os.path.exists("./splitAudio/"):
        os.mkdir("./splitAudio/")
    out_file = ".//splitAudio//chunk{0}.wav".format(i)
    print("exporting", out_file)
    chunk.export(out_file, format="wav")

i=0
for file in glob.glob(".//splitAudio//*.wav"):
    i += 1
    INPUT_FILE = str(i)+'helloworld.txt'
    if not os.path.isfile(INPUT_FILE):
        f = open(INPUT_FILE, 'w')
        f.close()
    data, samplerate = sf.read(file) #data in bit,  hence len(data)/samplerate = [s]
    sd.play(data,samplerate,device=3)

    command = 'open -a TextEdit '+INPUT_FILE
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
    # proc = psutil.Process(pid)
    # if not proc.is_running():
    # command = 'kill '+str(pid)
    command = 'osascript -e \' tell application "TextEdit" to quit\' '
    # 'killall TextEdit'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    print("...TextEdit should be closed already now")
    # f = open(INPUT_FILE, 'a')
    # f.write(",\n")
    # f.close()





#endregion pipe