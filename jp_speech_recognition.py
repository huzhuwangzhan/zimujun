#!/anaconda/envs/py35/bin/python

import subprocess

INPUT = 'audio_inputs.txt'
OUTPUT = 'output.txt'

command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist '+ INPUT + ' -demo -dnnconf julius.dnnconf $*'

p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
out, err = p.communicate()
out_decoded = out.decode('utf-8')
out_result = out_decoded[out_decoded.find('sentence1:')+11:]

print (out_result)