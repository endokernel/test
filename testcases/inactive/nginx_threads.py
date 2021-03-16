import subprocess
import time
import os

import variable
import time

start_time = time.time()

threadsizes = ['1', '2', '4', '8', '16', '32', '64']
datasizes = ['0k', '1k', '2k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1024k']

for i in range(0, len(variable.paths)):
    for j in range(0, len(threadsizes)):
        # launch nginx
        if variable.paths[i] == 'baseline':
            filesuffix = "nginx_thread_" + threadsizes[j] + "_baseline"
            servercmd = "LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/nginx_t -c ../conf/nginx_thread_" + threadsizes[j] + ".conf -p ../www"
            curbench = "nginx_thread_" + threadsizes[j] + " baseline"
        else:
            filesuffix = "nginx_thread_" + threadsizes[j] + "_" + variable.paths[i].split("/")[-2]
            servercmd = variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/nginx_t -c ../conf/nginx_thread_" + threadsizes[j] + ".conf -p ../www"
            curbench = "nginx_threads_" + threadsizes[j] + " " + variable.paths[i].split("/")[-2]
        resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
        fp = open(resfilename + ".tmp", "wb")
        for size in datasizes:
            fp.write(size.encode())
            fp.write(b',')
        fp.write(b'\n')

        print(servercmd)
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)

        for k in range (0, variable.tries):
            print(curbench + " " + str(k) + " ...")
            for size in datasizes:
                cmd = "ab -n 1000 -c 128 https://localhost:44443/" + size + ".bin 2> /dev/null"
                print(size + " " + str(k) + ":" )
                ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output = ps.stdout.read().splitlines()
                for lines in output:
                    if not lines.startswith(b'Transfer rate:'):
                        continue
                    res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
                    print(res)
                    fp.write(res)
                fp.write(b',')
            fp.write(b'\n')
        
        os.system("killall -9 nginx_t")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)
        fp.close()
        os.rename(resfilename + ".tmp", resfilename)
    

###### CET!!
for i in range(0, len(variable.cet_path)):
    for j in range (0, len(threadsizes)):
        # launch nginx
        filesuffix = "nginx_thread_" + threadsizes[j] + "_" + variable.cet_path[i].split("/")[-2]
        servercmd = variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/nginx_t -c ../conf/nginx_thread_" + threadsizes[j] + ".conf -p ../www"
        curbench = "nginx_threads_" + threadsizes[j] + " " + variable.cet_path[i].split("/")[-2]
        resfilename = "../" + variable.resdir + "/" + filesuffix + ".csv"
        fp = open(resfilename + ".tmp", "wb")
        for size in datasizes:
            fp.write(size.encode())
            fp.write(b',')
        fp.write(b'\n')
        print(servercmd)
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)

        for k in range (0, variable.tries):
            print(curbench + " " + str(k) + " ...")
            for size in datasizes:
                cmd = "ab -n 1000 -c 128 https://localhost:44443/" + size + ".bin 2> /dev/null"
                print(size + " " + str(k) + ":" )
                ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output = ps.stdout.read().splitlines()
                for lines in output:
                    if not lines.startswith(b'Transfer rate:'):
                        continue
                    res = lines.split(b":")[1].lstrip().split(b'[')[0].rstrip()
                    print(res)
                    fp.write(res)
                fp.write(b',')
            fp.write(b'\n')
        
        os.system("killall -9 nginx_t")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)
        fp.close()
        os.rename(resfilename + ".tmp", resfilename)


total = time.time() - start_time
hour = int(total/3600)
min = int((total%3600)/60)
sec = total%60
printable_time = str(hour) + "H " + str(min) + "M " + str(sec) + "S"

print("Nginx_threads total time: " + printable_time)
os.system("echo \"Nginx_threads: " + printable_time +"\" >> ../" + variable.resdir + "/time.txt")
