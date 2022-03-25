import subprocess
import time
import os

import variable
import time

start_time = time.time()

datasizes = ['0k', '1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k', '2048k', '4096k']

variable.set_name("nginx_strace")
variable.def_test("nginx", ['strace'], datasizes)

n = 0
for i in range(0, 1):
    # launch nginx
    filesuffix = "nginx_strace"
    servercmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -o /dev/null ../bin/nocet/nginx -c ../conf/nginx.conf -p ../www"
    curbench = "nginx Strace"
    resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
    fp = open(resfilename + ".tmp", "wb")
    for size in datasizes:
        fp.write(size.encode())
        fp.write(b',')
    fp.write(b'\n')

    ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
    time.sleep(1)

    for j in range (0, variable.tries):
        print(curbench + " " + str(j) + " ...")
        for size in datasizes:
            cmd = "ab -n 1000 https://localhost:44443/" + size + ".bin 2> /dev/null"
            print(size + " " + str(j) + ":" )
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = ps.stdout.read().splitlines()
            for lines in output:
                if not lines.startswith(b'Transfer rate:'):
                    continue
                res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
                print(res)
                variable.add_result("nginx", n, size, float(res))
                fp.write(res)
            fp.write(b',')
        fp.write(b'\n')
    
    os.system("killall -9 nginx")
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

print("Nginx total time: " + printable_time)
os.system("echo \"Nginx: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
variable.save()
