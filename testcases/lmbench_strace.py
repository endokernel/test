from pickle import FALSE
import subprocess
import os
import variable
import time

start_time = time.time()

# Prepare test file
os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=1024")

tests = dict()
tests.update({'null':'lat_syscall null'})
tests.update({'open':'lat_syscall open'})
tests.update({'read':'lat_syscall read'})
tests.update({'write':'lat_syscall write'})
tests.update({'mmap':'lat_mmap 512k /tmp/test.bin'})
tests.update({'signal install':'lat_sig install'})
tests.update({'signal catch':'lat_sig catch'})

variable.set_name("lmbench_strace")
variable.def_test("lmbench", ['strace'], tests.keys())
variable.tries = 2

n = 0
for i in range(0, 1):
    filesuffix = "lmbench_strace"
    cmdprefix = 'LD_LIBRARY_PATH=../libs/nocet strace -f -o /dev/null ../bin/nocet/'
    tname = 'baseline '

    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'null,open,read,write,mmap,sig inst,sig catch\n')

    for j in range(0, variable.tries):
        for curtest in tests.keys():
            okay = False
            while not okay:
                cmd = cmdprefix + tests[curtest]
                print(cmd)
                print(tname + " " + curtest + ": " + str(j))
                ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                try:
                    if curtest.startswith('mmap'):
                        output = ps.stderr.read().split(b' ')[1][:-1]
                    else:
                        output = ps.stderr.read().splitlines()[0].split(b'[')[1][5:11]
                    print(output)
                    variable.add_result('lmbench', n, curtest, float(output))
                    fp.write(output)
                    fp.write(b',')
                    okay = True
                except:
                    okay = False

        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("Lmbench total time: " + printable_time)
os.system("echo \"Lmbench: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")

variable.save()