import subprocess
import os

import variable


resfilename = "../" + variable.resdir + "/sqlite_nocet_baseline.csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990\n')

for i in range(0, variable.tries):
    cmd = 'LD_LIBRARY_PATH=../libs/nocet ../bin/nocet/speed'
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


resfilename = "../" + variable.resdir + "/sqlite_nocet.csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990\n')

for i in range(0, variable.tries):
    cmd = 'LD_LIBRARY_PATH=../libs/cet ' + variable.cet_glibcpath + '/ld-2.32.so ../bin/nocet/speed'
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



resfilename = "../" + variable.resdir + "/sqlite_cet.csv"
fp = open(resfilename + ".tmp", "wb")
fp.write(b'100,110,120,130,140,142,145,150,160,161,170,180,190,200,210,230,240,250,260,270,280,290,300,310,320,400,410,500,510,520,980,990\n')

for i in range(0, variable.tries):
    cmd = 'LD_LIBRARY_PATH=../libs/cet ' + variable.cet_glibcpath + '/ld-2.32.so ../bin/cet/speed'
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
