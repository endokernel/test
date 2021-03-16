#!/usr/bin/python3
import os
import subprocess
import time

import variable

stracepath = "/home/bi1/src/intravirt/bench/strace/"
'''
###################################
# curl. download 1GB
###################################
# Prepare data file
os.system("dd if=/dev/urandom of=../www/1g.bin bs=1024 count=1048576")

# Launch nginx server instance
serverpid = subprocess.Popen(["../bin/nginx", "-c",  "../conf/nginx.conf",  "-p", "../www/"]).pid
time.sleep(1)

curlcmd = "../bin/curl http://127.0.0.1:4000/1g.bin -o /tmp/my.bin"
for i in range(0, len(variable.paths)):
    if variable.paths[i] == 'baseline':
        cmd = "LD_LIBRARY_PATH=../libs strace -f " + curlcmd + " 2> " + stracepath + "curl_baseline.txt"
    else:
        cmd = "strace -f " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.new_glibcpath + ' ' + curlcmd + ' 2> ' + stracepath + 'curl_' + variable.paths[i].split("/")[-2] + ".txt"
    ps = os.system(cmd)

os.system("killall -9 nginx")
time.sleep(1)
os.unlink("../www/1g.bin")

###############################################
# nginx: Download 1k file and 1024k file
###############################################
datasize = ['1k', '1024k']
for curdata in datasize:
    for i in range(0, len(variable.paths)):
        # launch nginx
        if variable.paths[i] == 'baseline':
            servercmd = "strace -f ../bin/nginx -c ../conf/nginx.conf -p ../www/ 2> " + stracepath + "nginx_" + curdata + "_baseline.txt"
        else:
            servercmd = "strace -f " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.new_glibcpath + " ../bin/nginx -c ../conf/nginx.conf -p ../www/ 2> " + stracepath + "nginx_" + curdata + "_" + variable.paths[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 http://127.0.0.1:4000/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 nginx")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)


##########################################
# SQLite speedtest
##########################################
for i in range(0, len(variable.paths)):
    if variable.paths[i] == 'baseline':
        cmd = "strace -f ../bin/speed 2> " + stracepath + "sqlite_baseline.txt"
    else:
        cmd = "strace -f " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.new_glibcpath + " ../bin/speed 2> " + stracepath + "sqlite_" + variable.paths[i].split("/")[-2] + ".txt"
    print(cmd)
    os.system(cmd)


#########################################
# zip linux kernel source
#########################################
for i in range(0, len(variable.paths)):
    if variable.paths[i] == 'baseline':
        cmd = "strace -f ../bin/zip /tmp/test.zip -r ../linux-5.9.8 2> " + stracepath + "zip_baseline.txt"
    else:
        cmd = "strace -f " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.new_glibcpath + " ../bin/zip /tmp/test.zip -r ../linux-5.9.8 2> " + stracepath + "zip_" + variable.paths[i].split("/")[-2] + ".txt"
    print(cmd)
    os.system(cmd)
    os.unlink("/tmp/test.zip")
'''

res = dict()
syscallname = []
__files = []

targets = ['curl', 'nginx_1k', 'nginx_1024k', 'sqlite', 'zip']

for curtarget in targets:
    res.update({curtarget:dict()})

    for curpath in variable.paths:
        if curpath == 'baseline':
            curpathname = curpath
        else:
            curpathname = curpath.split("/")[-2]
        res[curtarget].update({curpathname:dict()})
        fullpath = stracepath + curtarget + '_' + curpathname + ".txt"
        fp = open(fullpath, "r")
        lines = fp.readlines()
        fp.close()

        for curline in lines:
            if curline.startswith('[pid '):
                if '(' not in curline:
                    continue
                if 'errno' in curline:
                    continue
                curout = curline.split(']')[1].split('(')[0][1:]
            elif '(' not in curline:
                continue
            else:
                curout = curline.split('(')[0]

            if curout not in syscallname:
                syscallname.append(curout)
            
            if curout in res[curtarget][curpathname].keys():
                res[curtarget][curpathname][curout] += 1
            else:
                res[curtarget][curpathname].update({curout:1})
    
    print(syscallname)


syscallname.sort()
for curtarget in targets:
    fp = open(stracepath + curtarget + ".csv", "wb")
    for curpath in res[curtarget].keys():
        fp.write(curpath.encode())
        fp.write(b',')
    fp.write(b'\n')

    for cursys in syscallname:
        fp.write(cursys.encode())
        fp.write(b',')
        for curpath in res[curtarget].keys():
            if cursys not in res[curtarget][curpath].keys():
                fp.write(b'0,')
                continue
            fp.write(str(res[curtarget][curpath][cursys]).encode())
            fp.write(b',')
        fp.write(b'\n')
    fp.close()            


