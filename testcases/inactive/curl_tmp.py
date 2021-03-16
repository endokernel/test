import subprocess
import os
import time

import variable
import time

start_time = time.time()

#Prepare data file
os.system("dd if=/dev/urandom of=../www/1g.bin bs=1024 count=1048576")

# Launch nginx server instance
serverpid = subprocess.Popen(["../bin/nocet/nginx", "-c",  "../conf/nginx_http.conf",  "-p", "../www/"]).pid
time.sleep(1)

respath = "../" + variable.resdir + "/curl_strace.csv"
fp = open(respath + ".tmp", "wb")
fp.write(b'strace')
fp.write(b'\n')


for i in range(0, variable.tries):
    curlcmd = "../bin/nocet/curl http://127.0.0.1:4000/1g.bin -o /tmp/my.bin"
    cmd = "time strace -fc " + curlcmd
    print ("strace " + str(i) + " ...")
    print(cmd)
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
    fp.write(b'\n')

os.system("killall -9 nginx")
time.sleep(1)

fp.close()
os.rename(respath + ".tmp", respath)

os.unlink("../www/1g.bin")

total = time.time() - start_time

printable_time = str(int(total/3600)) + "H " + str(int(total/60)) + "M " + str(int(total%60)) + "S"
print("Curl_strace total time: " + printable_time)
os.system("echo \"Curl_strace: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
