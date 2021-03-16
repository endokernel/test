import subprocess
import os

import variable
import time

import struct

start_time = time.time()

respath = "../" + variable.resdir + "/zip_strace.csv"
fp = open(respath + ".tmp", "wb")
fp.write(b'strace\n')


for i in range(0, variable.tries):

    cmd = "time strace -fc ../bin/nocet/zip /tmp/test.zip -r ../linux-5.9.8 1> /dev/null"
    print ("Zip: strace " + str(i) + " ...")
    ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
    output = ps.stderr.read().splitlines()
    for lines in output:
        if not lines.startswith(b'real'):
            continue
        strtime = lines.split(b'm')
        res = float(strtime[0][5:]) * 60
        res += float(strtime[1][:-1])
        print(res)
        fp.write(bytes(str(res), 'utf-8'))
        fp.write(b',')
        break
    os.system('rm -rf /tmp/test.zip')
    fp.write(b'\n')

fp.close()
os.rename(respath + ".tmp", respath)

total = time.time() - start_time
hour = int(total/3600)  
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"
print("zip_strace total time: " + printable_time)
os.system("echo \"zip_strace: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")