import subprocess

INPUT_FILE = 'audio_input.txt'
AUDIO_OUTPUT_FILE = 'audio_output.txt'
AUDIO_OUTPUT_TRANS_FILE = 'audio_output_translation.txt'
command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist {0} -demo -dnnconf julius.dnnconf $*'.format(INPUT_FILE)

p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) # p = subprocess.call(command, shell=True)
out, err = p.communicate()

# works for python 3. python 2 has to use print cmd to show right ja words in cmd line
# out_decoded = out.decode('utf-8')
# audio_out_result = out_decoded[out_decoded.find('sentence1:')+11:]

# works for python 2
if out.find('sentence1:') != -1:
    audio_out_result = out[out.find('sentence1:')+11:-1]
elif out.find('pass1_best:') != -1:
    # audio_out_result = out[out.find('pass1_best:') + 11:-1]
    audio_out_result = out.split('pass1_best:')[-1]
else:
    print '~~~~Give up, not found recognized Japanese text~~~~'
text_file = open(AUDIO_OUTPUT_FILE, "w")
text_file.write("%s" % audio_out_result)
text_file.close()
print 'Finish speech recog, start translation... '

from demo_baidu import *
fromLang='jp'
toLang='zh'

q = read_input(AUDIO_OUTPUT_FILE)
for src in q:
    myurl = form_url(src, fromLang, toLang)
    out_baidu = trans_baidu(myurl)
    out_baidu_dst = out_baidu[out_baidu.find('"dst":') + 7:-4]
    out_trans = out_baidu_dst.encode('utf8')
    # print out_trans
    text_file = open(AUDIO_OUTPUT_TRANS_FILE, "a")
    text_file.write("%s" % out_trans)
    text_file.close()
print 'Finish translation... '

