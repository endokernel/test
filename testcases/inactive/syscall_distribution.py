#!/usr/bin/python3
import os
import subprocess
import time

import variable

stracepath = "/home/bi1/src/intravirt/bench/strace/"

###################################
# curl. download 1GB
###################################
# Prepare data file
os.system("dd if=/dev/urandom of=../www/1g.bin bs=1024 count=1048576")

# Launch nginx server instance
serverpid = subprocess.Popen(["../bin/nocet/nginx", "-c",  "../conf/nginx.conf",  "-p", "../www/"]).pid
time.sleep(1)

curlcmd = "../bin/nocet/curl http://127.0.0.1:4000/1g.bin -o /tmp/my.bin"
for i in range(0, len(variable.paths)):
    if variable.paths[i] == 'baseline':
        cmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c " + curlcmd + " 2> " + stracepath + "curl_baseline.txt"
    else:
        cmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + ' ' + curlcmd + ' 2> ' + stracepath + 'curl_' + variable.paths[i].split("/")[-2] + ".txt"
    ps = os.system(cmd)
for i in range(0, len(variable.cet_path)):
    cmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + ' ' + curlcmd + ' 2> ' + stracepath + 'curl_' + variable.cet_path[i].split("/")[-2] + ".txt"
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
            servercmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c ../bin/nocet/nginx -c ../conf/nginx.conf -p ../www/ 2> " + stracepath + "nginx_" + curdata + "_baseline.txt"
        else:
            servercmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/nginx -c ../conf/nginx.conf -p ../www/ 2> " + stracepath + "nginx_" + curdata + "_" + variable.paths[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 http://127.0.0.1:4000/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 nginx")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)
    for i in range(0, len(variable.cet_path)):
        # launch nginx
        servercmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/nginx -c ../conf/nginx.conf -p ../www/ 2> " + stracepath + "nginx_" + curdata + "_" + variable.cet_path[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 http://127.0.0.1:4000/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 nginx")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)


###############################################
# nginx_https: Download 1k file and 1024k file
###############################################
datasize = ['1k', '1024k']
for curdata in datasize:
    for i in range(0, len(variable.paths)):
        # launch nginx
        if variable.paths[i] == 'baseline':
            servercmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c ../bin/nocet/nginx -c ../conf/nginx_https.conf -p ../www/ 2> " + stracepath + "nginx_https_" + curdata + "_baseline.txt"
        else:
            servercmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/nginx -c ../conf/nginx_https.conf -p ../www/ 2> " + stracepath + "nginx_https_" + curdata + "_" + variable.paths[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 https://127.0.0.1:44443/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 nginx")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)
    for i in range(0, len(variable.cet_path)):
        # launch nginx
        servercmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/nginx -c ../conf/nginx_https.conf -p ../www/ 2> " + stracepath + "nginx_https_" + curdata + "_" + variable.cet_path[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 https://127.0.0.1:44443/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 nginx")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)


###############################################
# lighttpd: Download 1k file and 1024k file
###############################################
datasize = ['1k', '1024k']
for curdata in datasize:
    for i in range(0, len(variable.paths)):
        # launch lighttpd
        if variable.paths[i] == 'baseline':
            servercmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c ../bin/nocet/lighttpd -f ../conf/lighttpd.conf -m ../libs/nocet/lighttpd_mod/ -D 2> " + stracepath + "lighttpd_" + curdata + "_baseline.txt"
        else:
            servercmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/lighttpd -f ../conf/lighttpd.conf -m ../libs/nocet/lighttpd_mod/ -D 2> " + stracepath + "lighttpd_" + curdata + "_" + variable.paths[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 http://127.0.0.1:4000/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 lighttpd")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)
    for i in range(0, len(variable.cet_path)):
        # launch lighttpd
        servercmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/lighttpd -f ../conf/lighttpd.conf -m ../libs/cet/lighttpd_mod/ -D 2> " + stracepath + "lighttpd_" + curdata + "_" + variable.cet_path[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 http://127.0.0.1:4000/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 lighttpd")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)




###############################################
# lighttpd with https: Download 1k file and 1024k file
###############################################
datasize = ['1k', '1024k']
for curdata in datasize:
    for i in range(0, len(variable.paths)):
        # launch lighttpd
        if variable.paths[i] == 'baseline':
            servercmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c ../bin/nocet/lighttpd -f ../conf/lighttpd_https.conf -m ../libs/nocet/lighttpd_mod/ -D 2> " + stracepath + "lighttpd_https_" + curdata + "_baseline.txt"
        else:
            servercmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/lighttpd -f ../conf/lighttpd_https.conf -m ../libs/nocet/lighttpd_mod/ -D 2> " + stracepath + "lighttpd_https_" + curdata + "_" + variable.paths[i].split("/")[-2] + ".txt"

        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 https://localhost:44443/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 lighttpd")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)
    for i in range(0, len(variable.cet_path)):
        # launch lighttpd
        servercmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/lighttpd -f ../conf/lighttpd_https.conf -m ../libs/cet/lighttpd_mod/ -D 2> " + stracepath + "lighttpd_https_" + curdata + "_" + variable.cet_path[i].split("/")[-2] + ".txt"
        ps = subprocess.Popen(servercmd, shell=True, stderr=subprocess.PIPE)
        time.sleep(1)
        cmd = "ab -n 2000 https://localhost:44443/" + curdata + ".bin 2> /dev/null"
        os.system(cmd)
        os.system("killall -9 lighttpd")
        os.system("killall -9 libintravirt.so")
        time.sleep(1)



##########################################
# SQLite speedtest
##########################################
for i in range(0, len(variable.paths)):
    if variable.paths[i] == 'baseline':
        cmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c ../bin/nocet/speed 2> " + stracepath + "sqlite_baseline.txt"
    else:
        cmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/speed 2> " + stracepath + "sqlite_" + variable.paths[i].split("/")[-2] + ".txt"
    os.system(cmd)
for i in range(0, len(variable.cet_path)):
    cmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/speed 2> " + stracepath + "sqlite_" + variable.cet_path[i].split("/")[-2] + ".txt"
    os.system(cmd)


'''
##########################################
# leveldb bench
##########################################
threadsize = ['1', '16']
leveldb_glibcpath = "/home/bi1/src/intravirt/glibc-leveldb/install/lib"
for curthread in threadsize:
    for i in range(0, len(variable.paths)):
        if variable.paths[i] == 'baseline':
            cmd = "MALLOC_CHECK_=1 strace -f -c ../bin/db_bench --benchmarks=\"fillseq,readseq\" --threads=" + curthread + " 2> " + stracepath + "leveldb_"+ curthread + "t_baseline.txt"
        else:
            cmd = "MALLOC_CHECK_=1 strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + leveldb_glibcpath + " ../bin/db_bench --benchmarks=\"fillseq,readseq\" --threads=" + curthread  + " 2> " + stracepath + "leveldb_" + curthread + "t_" + variable.paths[i].split("/")[-2] + ".txt"
        os.system(cmd)
'''

#########################################
# zip linux kernel source
#########################################
for i in range(0, len(variable.paths)):
    if variable.paths[i] == 'baseline':
        cmd = "LD_LIBRARY_PATH=../libs/nocet strace -f -c ../bin/nocet/zip /tmp/test.zip -r ../linux-5.9.8 2> " + stracepath + "zip_baseline.txt"
    else:
        cmd = "strace -f -c " + variable.paths[i] + "src/libintravirt/libintravirt.so " + variable.glibcpath + " ../bin/nocet/zip /tmp/test.zip -r ../linux-5.9.8 2> " + stracepath + "zip_" + variable.paths[i].split("/")[-2] + ".txt"
    os.system(cmd)
    os.unlink("/tmp/test.zip")
for i in range(0, len(variable.cet_path)):
    cmd = "strace -f -c " + variable.cet_path[i] + "src/libintravirt/libintravirt.so " + variable.cet_glibcpath + " ../bin/cet/zip /tmp/test.zip -r ../linux-5.9.8 2> " + stracepath + "zip_" + variable.cet_path[i].split("/")[-2] + ".txt"
    os.system(cmd)
    os.unlink("/tmp/test.zip")


res = dict()
syscallname = []
__files = []

target = []
target.append('curl')
target.append('nginx_1k')
target.append('nginx_1024k')
target.append('nginx_https_1k')
target.append('nginx_https_1024k')
target.append('lighttpd_1k')
target.append('lighttpd_1024k')
target.append('lighttpd_https_1k')
target.append('lighttpd_https_1024k')
target.append('sqlite')
#target.append('leveldb_1t')
#target.append('leveldb_16t')
target.append('zip')

totalpath = variable.paths + variable.cet_path

print(totalpath)

for curtarget in target:
    res.update({curtarget:dict()})

    for curpath in totalpath:
        if curpath == 'baseline':
            curpathname = curpath
        else:
            curpathname = curpath.split("/")[-2]
        res[curtarget].update({curpathname:dict()})
        fullpath = stracepath + curtarget + '_' + curpathname + ".txt"
        fp = open(fullpath, "r")
        print("Processing " + fullpath + " ...")

        for line in fp:
            line.lstrip(' ')
            line.rstrip(' ')
            items = (' '.join(line.split())).split(' ')
            index = items[0].replace('.', '')
            if not index.isdigit():
                continue
            
            if len(items) > 6 or len(items) < 5:
                continue

            if len(items) == 5:
                name = 4
            else:
                name = 5
            
            if items[name] == 'total':
                continue

            if items[name] not in syscallname:
                syscallname.append(items[name])
                if items[name] == '0':
                    print (line)
            res[curtarget][curpathname].update({items[name]:items[3]})
            
    print(syscallname)


syscallname.sort()
for curtarget in target:
    fp = open(stracepath + curtarget + ".csv", "wb")
    fp.write(b',')
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
