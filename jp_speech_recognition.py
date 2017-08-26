import subprocess

<<<<<<< HEAD
command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist audio_input.txt -demo -dnnconf julius.dnnconf $*'

p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) # p = subprocess.call(command, shell=True)
out, err = p.communicate()

# works for python 3. python 2 has to use print cmd to show right ja words in cmd line
# out_decoded = out.decode('utf-8')
# out_result = out_decoded[out_decoded.find('sentence1:')+11:]

# works for python 2
out_result = out[out.find('sentence1:')+11:]

text_file = open("output.txt", "w")
text_file.write("%s" % out_result)
text_file.close()


=======


command = './bin/osx/julius -C main.jconf -C am-dnn.jconf -input rawfile -filelist audio_inputs.txt -demo -dnnconf julius.dnnconf $*'

p = subprocess.call(command, shell=True)

>>>>>>> 26d64b665848f443bef3e9213844147fc902cf81
