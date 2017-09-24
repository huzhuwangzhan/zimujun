####################################
#region Cut audio
from pydub import AudioSegment
t1 = 1000*61 #Works in milliseconds
t2 = 1000*121
newAudio = AudioSegment.from_wav("Chinese_music.wav")
newAudio = newAudio[t1:t2]
newAudio.export('Chinese_music_1min.wav', format="wav") #
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

INPUT_AUDIOFILE = 'Chinese_music_1min.wav'
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
for file in glob.glob("./*.wav"):
    i += 1
    INPUT_FILE = 'helloworld.txt'
    if not os.path.isfile(INPUT_FILE):
        f = open(INPUT_FILE, 'w')
        f.close()
    data, samplerate = sf.read(file) #data in bit,  hence len(data)/samplerate = [s]
    sd.play(data,samplerate,device=2)

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
    command = 'osascript -e \' tell application "TextEdit" to quit\' '
    # 'killall TextEdit'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    print("...TextEdit should be closed already now")

def audio_2_text(AUDIO_DIR,TEXT_FILE):

    i=0
    for file in glob.glob(AUDIO_DIR+"*.wav"):
        i += 1
        TEMP_FILE = AUDIO_DIR+str(i)+TEXT_FILE
        if not os.path.isfile(TEMP_FILE):
            f = open(TEMP_FILE, 'w')
            f.close()

        data, samplerate = sf.read(file) #data in bit,  hence len(data)/samplerate = [s]
        sd.play(data,samplerate,device=2)

        command = 'open -a TextEdit '+TEMP_FILE
        p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
        time.sleep(3)
        pyautogui.press(['fn','fn'])
        time.sleep(len(data)/samplerate+5)
        pyautogui.press(['fn', 'fn'])
        time.sleep(2)
        print("...Dictation service should be closed already now")
        time.sleep(2)

        command = 'pgrep TextEditc
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        pid = int(str(p.stdout.readlines())[3:-4])
        command = 'osascript -e \' tell application "TextEdit" to quit\' '
        # 'killall TextEdit'
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        print("...TextEdit should be closed already now")

    files = glob.glob("*.txt")
    concat = ','.join([open(f).read() for f in files])

    import re
    pattern = re.compile(r'(,\s){2,}')
    concat = re.sub(pattern,',',concat)

    text_file = open('all.txt', 'w')
    text_file.write("%s" % concat)
    print('writing output to file ' + concat)
    text_file.close()

    os.system("sed 's/,\{2,\}/,/g' all.txt > final_all.txt")




#endregion pipe


#region ICA
from sklearn.decomposition import FastICA
ica = FastICA(n_components=2)
S_ = ica.fit_transform(data)  # Reconstruct signals

plt.figure()
plt.subplot(2,1,1)
plt.plot(data[:10000,1],'b')
plt.subplot(2,1,2)
plt.plot(S_[:10000,1],'r')

from nussl import AudioSignal, ICA
signal = AudioSignal('./zimujun/Chinese_music_1min.wav')

for i in range(X.shape[1]):
    observations.append(AudioSignal(audio_data_array=X[:, i], sample_rate = 44100))
ica = ICA(input_audio_signal=signal)
ica.run()
sources = ica.make_audio_signals()
#endregion


#region

python separateLeadStereoParam.py Chinese_music_1min.wav

#endregion