import subprocess
import os
import time

import variable
import time

start_time = time.time()

respath = "../" + variable.resdir + "/zlib.csv"
fp = open(respath + ".tmp", "wb")
for path in variable.iv_nocet_paths:
    if path == "baseline":
        continue
    else:
        fp.write(path.split("/")[-2].encode())
    fp.write(b',')
for path in variable.iv_cet_paths:
    fp.write(path.split("/")[-2].encode())
    fp.write(b',')
fp.write(b'\n')

for i in range(0, variable.tries):
    zlibcmd = "../bin/nocet/zlib_test ../conf/alice29.txt"
    for j in range(0, len(variable.iv_nocet_paths)):
        if variable.iv_nocet_paths[j] == 'baseline':
            continue
        else:
            cmd = "time " + 'LD_LIBRARY_PATH=../libs/nocet ' + variable.iv_nocet_paths[j] + "libintravirt.so ../zlib/nocet/glibc/install/lib " + zlibcmd
            print(variable.iv_nocet_paths[j].split("/")[-2] + " " + str(i) + " ...")
        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            if not lines.startswith(b'real'):
                continue
            result = lines[-6:-1]
            print(result)
            fp.write(result)
            fp.write(b',')
            break
    
    for j in range(0, len(variable.iv_cet_paths)):
        cmd = "time " + variable.iv_cet_paths[j] + "libintravirt.so ../zlib/cet/glibc/install/lib " + zlibcmd
        print(variable.iv_cet_paths[j].split("/")[-2] + " " + str(i) + " ...")

        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            if not lines.startswith(b'real'):
                continue
            result = lines[-6:-1]
            print(result)
            fp.write(result)
            fp.write(b',')
            break

    fp.write(b'\n')

fp.close()
os.rename(respath + ".tmp", respath)

total = time.time() - start_time

printable_time = str(int(total/3600)) + "H " + str(int(total/60)) + "M " + str(int(total%60)) + "S"
print("Zlib total time: " + printable_time)
os.system("echo \"Zlib: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
