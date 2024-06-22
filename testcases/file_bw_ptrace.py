import subprocess
import os

import variable
import time

start_time = time.time()

# Prepare test file
os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=40960")

cmds = ['1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k', '2048k', '4096k']

variable.set_name("file_bw_ptrace")
variable.def_test("file_bw", ['ptrace'], cmds)
variable.tries = 2
for i in range(0, 1):
    filesuffix = "file_bw_ptrace"
    cmdprefix = 'LD_LIBRARY_PATH=../libs/nocet strace -f -o /dev/null ../bin/nocet/'
    tname = 'strace '
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    for curcmd in cmds:
        fp.write(curcmd.encode())
        fp.write(b',')
    fp.write(b'\n')

    rr = [[] for k in range(0, len(cmds))]
    for j in range(0, variable.tries):
        for k in range(0, len(cmds)):
            okay = False
            while not okay:
                curtest = cmds[k]
                cmd = cmdprefix + curtest + " 40960k io_only /tmp/test.bin"
                print(tname + " " + curtest + ": " + str(j))
                ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                try:
                    output = ps.stderr.read().split(b' ')[1][:-1]
                    print(output)
                    rr[k].append(float(output))
                    fp.write(output)
                    fp.write(b',')
                    okay = True
                except:
                    okay = False
        fp.write(b'\n')
    variable.add_test("file_bw", rr)
        
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("File_BW total time: " + printable_time)
os.system("echo \"File_BW: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()
