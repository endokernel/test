import subprocess
import os

import variable
import time

start_time = time.time()


filesuffix = "sqlite_strace"
cmd = "strace -f ../bin/nocet/speed 2> /dev/null"
ctest = "strace"
resfilename ="../" + variable.resdir + "/" + filesuffix + ".csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990\n')

for j in range(0, variable.tries):    
    print("sqlite3 " + ctest + " " + str(j) + ":")
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read().splitlines()
    for lines in output:
        if not lines.startswith(b' '):
            continue
        res = lines[-8:-1].lstrip()
        fp.write(res)
        fp.write(b',')
    fp.write(b'\n')
fp.close()
os.rename(resfilename + ".tmp", resfilename)

total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("Sqlite_strace total time: " + printable_time)
os.system("echo \"SQlite_strace: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")