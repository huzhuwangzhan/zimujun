import subprocess

command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input mic -demo -dnnconf julius.dnnconf $*'

subprocess.Popen(command, shell=True)
