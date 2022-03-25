import subprocess
import time
import os

import variable
import time

start_time = time.time()

datasizes = ['0k', '1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k']
variable.set_name("lighttpd")
col = datasizes
row = variable.get_row()
variable.def_test("lighttpd", row, col)
variable.tries = 10
for i in range(0, len(variable.iv_nocet_paths)):
    # launch lighttpd
    if variable.iv_nocet_paths[i] == 'baseline':
        filesuffix = "lighttpd_baseline"
        servercmd = "LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/lighttpd -f ../conf/lighttpd.conf -m ../bin/nocet/lighttpd_module -D"
        curbench = "lighttpd Beseline"
    else:
        filesuffix = "lighttpd_" + variable.iv_nocet_paths[i].split("/")[-2]
        servercmd = variable.iv_nocet_paths[i] + "libintravirt.so " + variable.glibcpath + " ../bin/nocet/lighttpd -f ../conf/lighttpd.conf -m ../bin/nocet/lighttpd_module -D"
        curbench = "lighttpd " + variable.iv_nocet_paths[i].split("/")[-2]
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    for size in datasizes:
        fp.write(size.encode())
        fp.write(b',')
    fp.write(b'\n')
    ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
    time.sleep(1)
    rr = [[] for sz in datasizes]
    for j in range(0, variable.tries):
        print(curbench + " " + str(j) + " ...")
        for k in range(0, len(datasizes)):
            size = datasizes[k]
            cmd = "ab -n 1000 https://localhost:44443/" + size + ".bin 2> /dev/null"
            print(size + " " + str(j) + ":" )
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = ps.stdout.read().splitlines()
            for lines in output:
                if not lines.startswith(b'Transfer rate:'):
                    continue
                res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
                print(res)
                rr[k].append(float(res))
                fp.write(res)
            fp.write(b',')
        fp.write(b'\n')
    variable.add_test("lighttpd", rr)
        
    
    os.system("killall -9 lighttpd")
    os.system("killall -9 libintravirt.so")
    time.sleep(1)
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)

#### CET!!!
for i in range(0, len(variable.iv_cet_paths)):
    # launch lighttpd
    filesuffix = "lighttpd" + variable.iv_cet_paths[i].split("/")[-2]
    servercmd = variable.iv_cet_paths[i] + "libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/lighttpd -f ../conf/lighttpd.conf -m ../bin/cet/lighttpd_module -D"
    curbench = "lighttpd " + variable.iv_cet_paths[i].split("/")[-2]
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    for size in datasizes:
        fp.write(size.encode())
        fp.write(b',')
    fp.write(b'\n')
    print(servercmd)
    ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
    time.sleep(1)

    rr = [[] for sz in datasizes]
    for j in range (0, variable.tries):
        print(curbench + " " + str(j) + " ...")
        for k in range(0, len(datasizes)):
            size = datasizes[k]
            cmd = "ab -n 1000 https://localhost:44443/" + size + ".bin 2> /dev/null"
            print(size + " " + str(j) + ":" )
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = ps.stdout.read().splitlines()
            for lines in output:
                if not lines.startswith(b'Transfer rate:'):
                    continue
                res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
                print(res)
                rr[k].append(float(res))
                fp.write(res)
            fp.write(b',')
        fp.write(b'\n')
    variable.add_test("lighttpd", rr)
    
    os.system("killall -9 lighttpd")
    os.system("killall -9 libintravirt.so")
    time.sleep(1)
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("lighttpd total time: " + printable_time)
os.system("echo \"lighttpd: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()