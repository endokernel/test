import subprocess
import os
import variable
import time

start_time = time.time()

os.system("dd if=/dev/urandom of=/tmp/test.bin bs=1024 count=1024")

tests = dict()
tests.update({'null':'lat_syscall null'})
tests.update({'open':'lat_syscall open'})
tests.update({'read':'lat_syscall read'})
tests.update({'write':'lat_syscall write'})
tests.update({'mmap':'lat_mmap 512k /tmp/test.bin'})
tests.update({'signal install':'lat_sig install'})
#tests.update({'signal catch':'lat_sig catch'})


resfilename = "../" + variable.resdir + "/lmbench_nocet_baseline.csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'null,open,read,write,mmap,sig inst,sig catch\n')

for i in range(0, variable.tries):
    for curtest in tests.keys():
        cmd = 'LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/' + tests[curtest]
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        if curtest.startswith('mmap'):
            output = ps.stderr.read().split(b' ')[1][:-1]
        else:
            output = ps.stderr.read().splitlines()[0].split(b'[')[1][5:11]
        print(output)
        fp.write(output)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename);



resfilename = "../" + variable.resdir + "/lmbench_nocet.csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'null,open,read,write,mmap,sig inst,sig catch\n')

for i in range(0, variable.tries):
    for curtest in tests.keys():
        cmd = 'LD_LIBRARY_PATH=../libs/cet ' + variable.cet_glibcpath + '/ld-2.32.so ../bin/nocet/' + tests[curtest]
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        if curtest.startswith('mmap'):
            output = ps.stderr.read().split(b' ')[1][:-1]
        else:
            output = ps.stderr.read().splitlines()[0].split(b'[')[1][5:11]
        print(output)
        fp.write(output)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename);



resfilename = "../" + variable.resdir + "/lmbench_cet.csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'null,open,read,write,mmap,sig inst,sig catch\n')


for i in range(0, variable.tries):
    for curtest in tests.keys():
        cmd = 'LD_LIBRARY_PATH=../libs/cet ' + variable.cet_glibcpath + '/ld-2.32.so ../bin/cet/' + tests[curtest]
        ps = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        if curtest.startswith('mmap'):
            output = ps.stderr.read().split(b' ')[1][:-1]
        else:
            output = ps.stderr.read().splitlines()[0].split(b'[')[1][5:11]
        print(output)
        fp.write(output)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename);
