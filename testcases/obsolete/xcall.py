import subprocess
import os
import time

import variable
import time

start_time = time.time()

respath = "../" + variable.resdir + "/xcall.csv"
fp = open(respath + ".tmp", "wb")
for path in variable.paths:
    if path == "baseline":
        fp.write(b"baseline")
    else:
        fp.write(path.split("/")[-2].encode())
    fp.write(b',')
for path in variable.cet_path:
    fp.write(path.split("/")[-2].encode())
    fp.write(b',')
fp.write(b'\n')

for i in range(0, variable.tries*10):
    for j in range(0, len(variable.paths)):
        if variable.paths[j] == 'baseline':
            continue
        else:
            cmd = variable.paths[j] + "src/libintravirt/libintravirt.so " + variable.glibcpath + ' ../bin/nocet/xcall_cycle'
            print(variable.paths[j].split("/")[-2] + " " + str(i) + " ...")

        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
        output = ps.stdout.read()[:-1]
        print(output)
        fp.write(output)
        fp.write(b',')
    
    for j in range(0, len(variable.cet_path)):
        cmd = variable.cet_path[j] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + ' ../bin/nocet/xcall_cycle'
        print(variable.cet_path[j].split("/")[-2] + " " + str(i) + " ...")

        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
        output = ps.stdout.read()[:-1]
        print(output)
        fp.write(output)
        fp.write(b',')

    fp.write(b'\n')

fp.close()
os.rename(respath + ".tmp", respath)

total = time.time() - start_time

printable_time = str(int(total/3600)) + "H " + str(int(total/60)) + "M " + str(int(total%60)) + "S"
print("xcall total time: " + printable_time)
os.system("echo \"xcall: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
