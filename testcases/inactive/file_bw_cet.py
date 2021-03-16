import subprocess
import os

import variable
import time

start_time = time.time()

# Prepare test file
os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=40960")

cmds = ['1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k', '2048k', '4096k']


resfilename = "../" + variable.resdir + "/filebw_nocet_baseline.csv"
fp = open(resfilename + ".tmp", "wb")
for cur in cmds:
    fp.write(cur.encode())
    fp.write(b',')
fp.write(b'\n')

cmdprefix = 'LD_LIBRARY_PATH=../libs/nocet/ ../bin/nocet/'
for i in range(0, variable.tries):
    for cur in cmds:
        cmd = cmdprefix + cur + " 40960k io_only /tmp/test.bin"
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        output = ps.stderr.read().split(b' ')[1][:-1]
        fp.write(output)
        fp.write(b',')
        print(output)
    fp.write(b'\n')
fp.close()



resfilename = "../" + variable.resdir + "/filebw_nocet.csv"
fp = open(resfilename + ".tmp", "wb")
for cur in cmds:
    fp.write(cur.encode())
    fp.write(b',')
fp.write(b'\n')

cmdprefix = 'LD_LIBRARY_PATH=../libs/cet/ '+ variable.cet_glibcpath +  '/ld-2.32.so  ../bin/nocet/'
for i in range(0, variable.tries):
    for cur in cmds:
        cmd = cmdprefix + cur + " 40960k io_only /tmp/test.bin"
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        output = ps.stderr.read().split(b' ')[1][:-1]
        fp.write(output)
        fp.write(b',')
        print(output)
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)



resfilename = "../" + variable.resdir + "/filebw_cet.csv"
fp = open(resfilename + ".tmp", "wb")
for cur in cmds:
    fp.write(cur.encode())
    fp.write(b',')
fp.write(b'\n')

cmdprefix = 'LD_LIBRARY_PATH=../libs/cet/ '+ variable.cet_glibcpath +  '/ld-2.32.so  ../bin/cet/'
for i in range(0, variable.tries):
    for cur in cmds:
        cmd = cmdprefix + cur + " 40960k io_only /tmp/test.bin"
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        output = ps.stderr.read().split(b' ')[1][:-1]
        fp.write(output)
        fp.write(b',')
        print(output)
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)