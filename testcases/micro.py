import subprocess
import time
import os

import variable
import time

start_time = time.time()

testcase = ['ivcall empty', 'getppid fastpath', 'ivcall getppid', 'empty xcall', 'temporal call without mem', 'temporal call with mem']

variable.set_name("micro")
variable.def_test("micro", variable.get_row(baseline=False), testcase)

n = 0
for i in range(0, len(variable.iv_nocet_paths)):
    # launch micro
    if variable.iv_nocet_paths[i] == 'baseline':
        continue
    else:
        filesuffix = "micro_" + variable.iv_nocet_paths[i].split("/")[-2]
        cmd = 'LD_LIBRARY_PATH=../libs/nocet ' + variable.iv_nocet_paths[i] + "libintravirt.so " + variable.glibcpath + " ../src/intravirt-src/src/libtemporal/build/temporal_test 7"
        curbench = "micro " + variable.iv_nocet_paths[i].split("/")[-2]
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    for size in testcase:
        fp.write(size.encode())
        fp.write(b',')
    fp.write(b'\n')

    for j in range (0, variable.tries):
        print(curbench + " " + str(j) + " ...")
        print(cmd)
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for idx, lines in enumerate(ps.stdout.readlines()):
            print(lines)
            res = float(lines)
            print(res)
            variable.add_result("micro", n, idx, float(res))
            fp.write(bytes(str(res), 'utf-8'))
            fp.write(b',')
        fp.write(b'\n')
    
    os.system("killall -9 libintravirt.so")
    time.sleep(1)
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1
    

###### CET!!
for i in range(0, len(variable.iv_cet_paths)):
    # launch micro
    filesuffix = "micro_" + variable.iv_cet_paths[i].split("/")[-2]
    cmd = variable.iv_cet_paths[i] + "libintravirt.so " + variable.cet_glibcpath + " ../src/intravirt-src/src/libtemporal/build/temporal_test 7"
    curbench = "micro " + variable.iv_cet_paths[i].split("/")[-2]
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    for size in testcase:
        fp.write(size.encode())
        fp.write(b',')
    fp.write(b'\n')

    for j in range (0, variable.tries):
        print(curbench + " " + str(j) + " ...")
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for idx, lines in enumerate(ps.stdout.readlines()):
            res = float(lines)
            print(res)
            variable.add_result("micro", n, idx, float(res))
            fp.write(bytes(str(res), 'utf-8'))
            fp.write(b',')
        fp.write(b'\n')
    
    os.system("killall -9 libintravirt.so")
    time.sleep(1)
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("Micro total time: " + printable_time)
os.system("echo \"Micro: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()
