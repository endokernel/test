import subprocess
import os

import variable
import time

start_time = time.time()
variable.set_name("zip_strace")
variable.def_test("zip", ['strace'], ["kernel"])

n = 0
respath = "../" + variable.resdir + "/zip_strace.csv"
fp = open(respath + ".tmp", "wb")

for i in range(0, variable.tries):
    n = 0
    for j in range(0, 1):
        cmd = "time LD_LIBRARY_PATH=../libs/nocet strace -f -o /dev/null ../bin/nocet/zip /tmp/test.zip -r ../linux-5.9.8 1> /dev/null"
        print ("Zip: baseline " + str(i) + " ...")
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
            variable.add_result("zip", n, 0, float(res))
            break
        os.system('rm -rf /tmp/test.zip')
        n = n + 1
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
variable.save()
