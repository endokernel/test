import subprocess
import os
import time

import variable
import time

variable.set_name("curl_strace")
start_time = time.time()

# Launch nginx server instance
serverpid = subprocess.Popen(["../bin/nocet/nginx", "-c",  "../conf/nginx.conf",  "-p", "../www/"]).pid
time.sleep(1)
row = []
respath = "../" + variable.resdir + "/curl_strace.csv"
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

variable.def_test("curl", ['strace'], col)
variable.tries = 2
ary1 = [[] for i in range(0, 1)]
for i in range(0, variable.tries):
    curlcmd = "../bin/nocet/curl https://localhost:44443/1g.bin --insecure -o /tmp/my.bin"
    for j in range(0, 1):
        cmd = "time LD_LIBRARY_PATH=../libs/nocet/ strace -f -o /dev/null " + curlcmd
        print ("strace " + str(i) + " ...")
        print(cmd)
        ps = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=subprocess.PIPE)
        output = ps.stderr.read().splitlines()
        for lines in output:
            #print(lines)
            if not lines.startswith(b'real'):
                continue
            strtime = lines.split(b'm')
            res = float(strtime[0][5:]) * 60
            res += float(strtime[1][:-1])
            print(res)
            fp.write(bytes(str(res), 'utf-8'))
            ary1[j].append(float(res))
            fp.write(b',')
            break

    fp.write(b'\n')

for j in range(0, 1):
    variable.add_test("curl", [ ary1[j] ])
os.system("killall -9 nginx")
time.sleep(1)

fp.close()
os.rename(respath + ".tmp", respath)

total = time.time() - start_time

printable_time = str(int(total/3600)) + "H " + str(int(total/60)) + "M " + str(int(total%60)) + "S"
print("Curl total time: " + printable_time)
os.system("echo \"Curl: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()