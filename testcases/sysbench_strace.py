import subprocess
import os
import variable
import time

start_time = time.time()

threadsizes = ['1', '2', '4', '8', '16']

# Prepare test file
tests = dict()
tests.update({'memory':'memory --threads='})
tests.update({'fileio':'fileio --file-total-size=1G --file-test-mode=rndrd --threads='})
os.system('../bin/nocet/sysbench fileio --file-total-size=1G prepare')

variable.set_name("sysbench_strace")
variable.def_test("memory", ['strace'], threadsizes)
variable.def_test("fileio", ['strace'], threadsizes)

n = 0

for i in range(0, 1):
    filesuffix = "sysbench_strace"
    cmdprefix = 'LD_LIBRARY_PATH=../libs/nocet strace -f -o /dev/null ../bin/nocet/sysbench '
    tname = 'baseline '
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'1,,2,,4,,8,,16,,\n')
    fp.write(b'memory,fileio,memory,fileio,memory,fileio,memory,fileio,memory,fileio,memory,fileio\n')

    for j in range(0, variable.tries):
        for curthreads in threadsizes:
            for curtest in tests.keys():
                okay = False
                while not okay:
                    cmd = cmdprefix + tests[curtest] + curthreads + " run"
                    print(tname + " " + curtest + ": " + str(j) + ", " + curthreads + " threads")
                    print(cmd)
                    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    output = ps.stdout.read().splitlines()
                    myout = b''
                    try:
                        for curline in output:
                            if b'transferred' in curline:
                                myout = curline.split(b'transferred')[1][2:9]
                                break
                            if b'read, MiB/s:' in curline:
                                myout = curline.split(b' ')[-1]
                                break
                        variable.add_result(curtest, n, curthreads, float(myout))
                        fp.write(myout)
                        fp.write(b',')
                        print(myout)
                        okay = True
                    except:
                        okay = False
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1

os.system("rm test_file.* -rf")

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("sysbench total time: " + printable_time)
os.system("echo \"Lmbench: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()
