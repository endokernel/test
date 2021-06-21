import subprocess
import os

import variable
import time

start_time = time.time()

respath = "../" + variable.resdir + "/zip.csv"
fp = open(respath + ".tmp", "wb")
for path in variable.iv_nocet_paths:
    if path == "baseline":
        fp.write(b"baseline")
    else:
        fp.write(path.split("/")[-2].encode())
    fp.write(b',')
for path in variable.iv_cet_paths:
    if path == "baseline":
        fp.write(b"baseline")
    else:
        fp.write(path.split("/")[-2].encode())
    fp.write(b',')
fp.write(b'\n')


for i in range(0, variable.tries):
    for j in range(0, len(variable.iv_nocet_paths)):
        if variable.iv_nocet_paths[j] == 'baseline':
            cmd = "time LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/zip /tmp/test.zip -r ../linux-5.9.8 1> /dev/null"
            print ("Zip: baseline " + str(i) + " ...")
        else:
            cmd = "time " + variable.iv_nocet_paths[j] + "libintravirt.so " + variable.glibcpath + ' ../bin/nocet/zip /tmp/test.zip -r ../linux-5.9.8 1> /dev/null'
            print("Zip: " + variable.iv_nocet_paths[j].split("/")[-2] + " " + str(i) + " ...")
        
        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            if not lines.startswith(b'real'):
                continue
            res = lines[-7:-1]
            print(res)
            fp.write(res)
            fp.write(b',')
            break
        os.system('rm -rf /tmp/test.zip')

    for j in range(0, len(variable.iv_cet_paths)):
        cmd = "time " + variable.iv_cet_paths[j] + "libintravirt.so " + variable.cet_glibcpath + ' ../bin/cet/zip /tmp/test.zip -r ../linux-5.9.8 1> /dev/null'
        print("Zip: " + variable.iv_cet_paths[j].split("/")[-2] + " " + str(i) + " ...")
        
        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            if not lines.startswith(b'real'):
                continue
            res = lines[-7:-1]
            print(res)
            fp.write(res)
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
print("zip total time: " + printable_time)
os.system("echo \"zip: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
