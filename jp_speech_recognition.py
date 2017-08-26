import subprocess



command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist audio_inputs.txt -demo -dnnconf julius.dnnconf $*'

p = subprocess.call(command, shell=True)

