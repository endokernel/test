import subprocess
import os

import variable
import time

start_time = time.time()

# Prepare test file
os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=40960")

cmds = ['1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k', '2048k', '4096k']



filesuffix = "file_bw_strace"
cmdprefix = 'strace -fc ../bin/nocet/'
tname = 'strace '

resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
fp = open(resfilename + ".tmp", "wb")
for curcmd in cmds:
    fp.write(curcmd.encode())
    fp.write(b',')
fp.write(b'\n')

for j in range(0, variable.tries):
    for curtest in cmds:
        cmd = cmdprefix + curtest + " 40960k io_only /tmp/test.bin"
        print(tname + " " + curtest + ": " + str(j))
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()[0].split(b' ')[1]
        fp.write(output)
        fp.write(b',')
        print(output)
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("File_BW_strace total time: " + printable_time)
os.system("echo \"File_BW_strace: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")