import subprocess
import os

import variable
import time

start_time = time.time()

variable.set_name("sqlite")
variable.def_test("sqlite", variable.get_row(), "100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990,total".split(","))
variable.tries = 2
n = 0
for i in range(0, len(variable.iv_nocet_paths)):
    if variable.iv_nocet_paths[i] == "baseline":
        filesuffix = "sqlite_baseline"
        cmd = "LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/sqlite_speedtest"
        ctest = "baseline"
    else:
        filesuffix = "sqlite_" + variable.iv_nocet_paths[i].split("/")[-2]
        cmd = variable.iv_nocet_paths[i] + "libintravirt.so " + variable.glibcpath + " ../bin/nocet/sqlite_speedtest"
        ctest = variable.iv_nocet_paths[i].split("/")[-2]
    resfilename ="../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990,total\n')
    print(cmd)
    for j in range(0, variable.tries):
        print("sqlite3 " + ctest + " " + str(j) + ":")
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read().splitlines()
        cc = 0
        for lines in output:
            if not lines.startswith(b' '):
                continue
            res = lines[-8:-1].lstrip()
            fp.write(res)
            variable.add_result("sqlite", n, cc, float(res))
            fp.write(b',')
            cc = cc + 1
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1


### CET
for i in range(0, len(variable.iv_cet_paths)):
    filesuffix = "sqlite_" + variable.iv_cet_paths[i].split("/")[-2]
    cmd = variable.iv_cet_paths[i] + "libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/sqlite_speedtest"
    ctest = variable.iv_cet_paths[i].split("/")[-2]
    resfilename ="../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    fp.write(b'100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990\n')
    
    for j in range(0, variable.tries):
        print("sqlite3 " + ctest + " " + str(j) + ":")
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = ps.stdout.read().splitlines()
        cc = 0
        for lines in output:
            if not lines.startswith(b' '):
                continue
            res = lines[-8:-1].lstrip()
            fp.write(res)
            fp.write(b',')
            variable.add_result("sqlite", n, cc, float(res))
            cc = cc + 1
        fp.write(b'\n')
    fp.close()
    os.rename(resfilename + ".tmp", resfilename)
    n = n + 1


total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("Sqlite total time: " + printable_time)
os.system("echo \"SQlite: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()