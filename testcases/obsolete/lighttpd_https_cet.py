import subprocess
import time
import os

import variable
import time


start_time = time.time()

datasizes = ['0k', '1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k']



resfilename = "../" + variable.resdir + "/lighttpd_https_nocet_baseline.csv"
fp = open(resfilename + ".tmp", "wb")
for size in datasizes:
    fp.write(size.encode())
    fp.write(b',')
fp.write(b'\n')
servercmd = "LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/lighttpd -f ../conf/lighttpd_https.conf -m ../libs/nocet/lighttpd_mod/ -D"
ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
time.sleep(1)

for j in range (0, variable.tries):
    for size in datasizes:
        cmd = "ab -n 2000 https://localhost:44443/" + size + ".bin 2> /dev/null"
        print(size + " " + str(j) + ":" )
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read().splitlines()
        for lines in output:
            if not lines.startswith(b'Transfer rate:'):
                continue
            res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
            print(res)
            fp.write(res)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)
os.system('killall -9 lighttpd')



resfilename = "../" + variable.resdir + "/lighttpd_https_nocet.csv"
fp = open(resfilename + ".tmp", "wb")
for size in datasizes:
    fp.write(size.encode())
    fp.write(b',')
fp.write(b'\n')
servercmd = "LD_LIBRARY_PATH=../libs/cet "+ variable.cet_glibcpath +  "/ld-2.32.so ../bin/nocet/lighttpd -f ../conf/lighttpd_https.conf -m ../libs/nocet/lighttpd_mod/ -D"
ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
time.sleep(1)

for j in range (0, variable.tries):
    for size in datasizes:
        cmd = "ab -n 2000 https://localhost:44443/" + size + ".bin 2> /dev/null"
        print(size + " " + str(j) + ":" )
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read().splitlines()
        for lines in output:
            if not lines.startswith(b'Transfer rate:'):
                continue
            res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
            print(res)
            fp.write(res)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)
os.system('killall -9 ld-2.32.so')




resfilename = "../" + variable.resdir + "/lighttpd_https_cet.csv"
fp = open(resfilename + ".tmp", "wb")
for size in datasizes:
    fp.write(size.encode())
    fp.write(b',')
fp.write(b'\n')
servercmd = "LD_LIBRARY_PATH=../libs/cet "+ variable.cet_glibcpath +  "/ld-2.32.so ../bin/cet/lighttpd -f ../conf/lighttpd_https.conf -m ../libs/cet/lighttpd_mod/ -D"
ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
time.sleep(1)

for j in range (0, variable.tries):
    for size in datasizes:
        cmd = "ab -n 2000 https://localhost:44443/" + size + ".bin 2> /dev/null"
        print(size + " " + str(j) + ":" )
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read().splitlines()
        for lines in output:
            if not lines.startswith(b'Requests per second:'):
                continue
            res = lines.split(b":")[1].lstrip()[:-15]
            print(res)
            fp.write(res)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)
os.system('killall -9 ld-2.32.so')
