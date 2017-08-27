#!/anaconda/envs/py35/bin/python
import subprocess
def run_stt(command):



    p = subprocess.Popen(command, shell=True,stdout= subprocess.PIPE)
    out, err = p.communicate()
    out_decoded = out.decode('utf-8')
    out_result = out_decoded[out_decoded.find('sentence1:')+11:]
    print (out_result)

    return out_result