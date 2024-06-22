import subprocess
import os
import time

import variable
import time

variable.set_name("curl")
start_time = time.time()

# Launch nginx server instance
serverpid = subprocess.Popen(["../bin/nocet/nginx", "-c",  "../conf/nginx.conf",  "-p", "../www/"]).pid
time.sleep(1)
row = []
respath = "../" + variable.resdir + "/curl.csv"
fp = open(respath + ".tmp", "wb")
for path in variable.iv_nocet_paths:
    if path == "baseline":
        fp.write(b"baseline")
        row.append("baseline")
    else:
        fp.write(path.split("/")[-2].encode())
        row.append(path.split("/")[-2])
    fp.write(b',')
for path in variable.iv_cet_paths:
    fp.write(path.split("/")[-2].encode())
    row.append(path.split("/")[-2])
    fp.write(b',')
fp.write(b'\n')
col = ["1g"]

variable.def_test("curl", row, col)
variable.tries = 10
ary1 = [[] for i in range(0, len(variable.iv_nocet_paths))]
ary2 = [[] for i in range(0, len(variable.iv_cet_paths))]
for i in range(0, variable.tries):
    curlcmd = "../bin/nocet/curl https://localhost:44443/1g.bin --insecure -o /tmp/my.bin"
    for j in range(0, len(variable.iv_nocet_paths)):
        if variable.iv_nocet_paths[j] == 'baseline':
            cmd = "time LD_LIBRARY_PATH=../libs/nocet/ " + curlcmd
            print ("Beseline " + str(i) + " ...")
        else:
            cmd = "time " + variable.iv_nocet_paths[j] + "libintravirt.so " + variable.glibcpath + ' ' + curlcmd
            print(variable.iv_nocet_paths[j].split("/")[-2] + " " + str(i) + " ...")
        print(cmd)
        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            if not lines.startswith(b'real'):
                continue
            result = lines[-6:-1]
            print(result)
            fp.write(result)
            ary1[j].append(float(result))
            fp.write(b',')
            break
    
    for j in range(0, len(variable.iv_cet_paths)):
        cmd = "time " + variable.iv_cet_paths[j] + "libintravirt.so " + variable.cet_glibcpath + ' ' + curlcmd
        print(variable.iv_cet_paths[j].split("/")[-2] + " " + str(i) + " ...")

        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            if not lines.startswith(b'real'):
                continue
            result = lines[-6:-1]
            ary2[j].append(float(result))
            print(result)
            fp.write(result)
            fp.write(b',')
            break

    fp.write(b'\n')

for j in range(0, len(variable.iv_nocet_paths)):
    variable.add_test("curl", [ ary1[j] ])
for j in range(0, len(variable.iv_cet_paths)):
    variable.add_test("curl", [ ary2[j] ])
os.system("killall -9 nginx")
time.sleep(1)

fp.close()
os.rename(respath + ".tmp", respath)

total = time.time() - start_time

printable_time = str(int(total/3600)) + "H " + str(int(total/60)) + "M " + str(int(total%60)) + "S"
print("Curl total time: " + printable_time)
os.system("echo \"Curl: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()