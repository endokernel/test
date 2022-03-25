import subprocess
import os
import time

import variable
import time

start_time = time.time()
variable.set_name("zlib")
variable.def_test("zlib", variable.get_row(), ["alice29"])

n = 0

respath = "../" + variable.resdir + "/zlib.csv"
fp = open(respath + ".tmp", "wb")
for path in variable.iv_nocet_paths:
    if path == "baseline":
        fp.write(b"baseline")
    else:
        fp.write(path.split("/")[-2].encode())
    fp.write(b',')
for path in variable.iv_cet_paths:
    fp.write(path.split("/")[-2].encode())
    fp.write(b',')
fp.write(b'\n')
variable.tries = 20
for i in range(0, variable.tries):
    zlibcmd = "../bin/nocet/zlib_test ../conf/alice29.txt"
    n = 0
    for j in range(0, len(variable.iv_nocet_paths)):
        if variable.iv_nocet_paths[j] == 'baseline':
            cmd = "time LD_LIBRARY_PATH=../libs/nocet/ " + zlibcmd
            print ("Beseline " + str(i) + " ...")
        else:
            cmd = "time " + variable.iv_nocet_paths[j] + "libintravirt.so " + variable.glibcpath + ' ' + zlibcmd
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
            variable.add_result("zlib", n, 0, float(result))
            break
        n = n + 1
    
    for j in range(0, len(variable.iv_cet_paths)):
        cmd = "time " + variable.iv_cet_paths[j] + "libintravirt.so " + variable.cet_glibcpath + ' ' + zlibcmd
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
            variable.add_result("zlib", n, 0, float(result))
            break
        n = n + 1

    fp.write(b'\n')

fp.close()
os.rename(respath + ".tmp", respath)

total = time.time() - start_time

printable_time = str(int(total/3600)) + "H " + str(int(total/60)) + "M " + str(int(total%60)) + "S"
print("Zlib total time: " + printable_time)
os.system("echo \"Zlib: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()