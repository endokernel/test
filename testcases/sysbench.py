import subprocess
import os
import variable
import time

start_time = time.time()

threadsizes = ['1', '2', '4', '8', '16', '32']

# Prepare test file
tests = dict()
tests.update({'memory':'memory --threads='})
tests.update({'fileio':'fileio --file-total-size=1G --file-test-mode=rndrd --threads='})
os.system('../bin/nocet/sysbench fileio --file-total-size=1G prepare')

for i in range(0, len(variable.iv_nocet_paths)):
    if variable.iv_nocet_paths[i] == "baseline":
        filesuffix = "sysbench_baseline"
        cmdprefix = 'LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/sysbench '
        tname = 'baseline '
    else:
        filesuffix = "sysbench_" + variable.iv_nocet_paths[i].split("/")[-2]
        cmdprefix = variable.iv_nocet_paths[i] + "libintravirt.so " + variable.glibcpath + " ../bin/nocet/sysbench "
        tname = variable.iv_nocet_paths[i].split("/")[-2]

    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'1,,2,,4,,8,,16,,32,,\n')
    fp.write(b'memory,fileio,memory,fileio,memory,fileio,memory,fileio,memory,fileio,memory,fileio\n')

    for j in range(0, variable.tries):
        for curthreads in threadsizes:
            for curtest in tests.keys():
                cmd = cmdprefix + tests[curtest] + curthreads + " run"
                print(tname + " " + curtest + ": " + str(j) + ", " + curthreads + " threads")
                ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output = ps.stdout.read().splitlines()
                myout = b''
                for curline in output:
                    if b'transferred' in curline:
                        myout = curline.split(b'transferred')[1][2:9]
                        break
                    if b'read, MiB/s:' in curline:
                        myout = curline.split(b' ')[-1]
                        break
                fp.write(myout)
                fp.write(b',')
                print(myout)
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)

### now CET's turn
for i in range(0, len(variable.iv_cet_paths)):
    filesuffix = "sysbench_" + variable.iv_cet_paths[i].split("/")[-2]
    cmdprefix = variable.iv_cet_paths[i] + "libintravirt.so " + variable.cet_glibcpath + " ../bin/nocet/sysbench "
    tname = variable.iv_cet_paths[i].split("/")[-2]

    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'1,,2,,4,,8,,16,,32,,\n')
    fp.write(b'memory,fileio,memory,fileio,memory,fileio,memory,fileio,memory,fileio,memory,fileio\n')

    for j in range(0, variable.tries):
        for curthreads in threadsizes:
            for curtest in tests.keys():
                cmd = cmdprefix + tests[curtest] + curthreads + " run"
                print(tname + " " + curtest + ": " + str(j) + ", " + curthreads + " threads")
                ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output = ps.stdout.read().splitlines()
                myout = b''
                for curline in output:
                    if b'transferred' in curline:
                        myout = curline.split(b'transferred')[1][2:9]
                        break
                    if b'read, MiB/s:' in curline:
                        myout = curline.split(b' ')[-1]
                        break
                fp.write(myout)
                fp.write(b',')
                print(myout)
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)

os.system("rm test_file.* -rf")

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("sysbench total time: " + printable_time)
os.system("echo \"Lmbench: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
