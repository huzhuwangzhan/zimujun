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

for file in glob.glob(".//splitAudio//*.wav"):
    INPUT_FILE = 'helloworld.txt'
    if not os.path.isfile(INPUT_FILE):
        f = open(INPUT_FILE,'w')
        f.close()
    os.system('echo ",\n" >> '+INPUT_FILE)
    data, samplerate = sf.read(file) #data in bit,  hence len(data)/samplerate = [s]
    # sd.query_devices()
    sd.play(data,samplerate,device=3)
    command = 'open -a TextEdit '+INPUT_FILE
    p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
    time.sleep(3)
    pyautogui.press(['fn','fn'])

#endregion - pipe