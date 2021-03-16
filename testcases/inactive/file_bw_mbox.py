import subprocess
import os

import variable
import time

start_time = time.time()

# Prepare test file
os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=40960")

cmds = ['1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k', '2048k', '4096k']

resfilename = "../result/file_bw_mbox.csv"
fp = open(resfilename + ".tmp", "wb")
for curcmd in cmds:
    fp.write(curcmd.encode())
    fp.write(b',')
fp.write(b'\n')

for i in range(0, variable.tries):
    for curtest in cmds:
        cmd = "/home/bi1/src/intravirt/mbox/src/mbox ../bin/nocet/" + curtest + " 40960k io_only /tmp/test.bin"
        tname = "mbox filebw " + curtest + ": " + str(i)
        print (cmd)
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        output = ps.stderr.read().split(b' ')[1][:-1]
        fp.write(output)
        fp.write(b',')
        print(output)
    fp.write(b'\n')
    delcmd = ("rm /tmp/sandbox* -rf")
    os.system(delcmd)
        


fp.close()
os.rename(resfilename + ".tmp", resfilename)