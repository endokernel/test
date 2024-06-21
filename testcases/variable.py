# Intravirt codebases need to measure
iv_nocet_paths = []

iv_nocet_paths.append("baseline")
#iv_nocet_paths.append("../intravirt/random1/")
#iv_nocet_paths.append("../intravirt/random2/")
#iv_nocet_paths.append("../intravirt/random4/")
#iv_nocet_paths.append("../intravirt/random8/")
#iv_nocet_paths.append("../intravirt/random16/")
#iv_nocet_paths.append("../intravirt/random32/")
#iv_nocet_paths.append("../intravirt/random1024/")
#iv_nocet_paths.append("../intravirt/queen/")
iv_nocet_paths.append("../intravirt/intravirt/dispatch_eiv/")

iv_cet_paths = []
#iv_cet_paths.append("../intravirt/seccomp_cet/")
#iv_cet_paths.append("../intravirt/dispatch_cet/")

# Benchmarks
benchs = []
benchs.append("lmbench.py")
benchs.append("lighttpd.py")
benchs.append("sqlite.py")
benchs.append("curl.py")
benchs.append("file_bw.py")
benchs.append("nginx.py")
benchs.append("nginx_threads.py")
benchs.append("nginx_safebox.py")
benchs.append("nginx_sandbox.py")
benchs.append("nginx_safe_sand.py")
benchs.append("zip.py")

# Some global variables
resdir = "result"
tries = 2 #10 #5
bindir = "bin"

# Additional variables
cet_glibcpath = "../glibc-cet/install/lib"
glibcpath = "../glibc-nocet/install/lib"

coarse_cet = True

import pickle
objs = {}
name = ""
def set_name(_name):
    global name
    name = _name

def get_row(baseline=True):
    r = []
    for path in iv_nocet_paths:
        if path == "baseline" :
            r.append("baseline") if baseline else None
        else:
            r.append(path.split("/")[-2])
    for path in iv_cet_paths:
        r.append(path.split("/")[-2])
    return r
def def_test(g, row, col):
    global objs
    objs[g] = {"name": g, "row":row, "col":list(col), "data":None}

def add_test(g, result):
    global objs
    if not objs[g]["data"]:
        objs[g]["data"] = []
    objs[g]["data"].append(result)

def add_result(g, row, col, datapoint):
    global objs
    if isinstance(col, str):
        col = objs[g]['col'].index(col)
  
    if not objs[g]["data"]:
        objs[g]["data"] = [
            [
                [] for j in range(0,len(objs[g]['col']))
            ] for i in range(0, len(objs[g]["row"]))
        ]
    objs[g]["data"][row][col].append(datapoint)

def save():
    f = open("../" + resdir + "/" + name + ".pickle", "wb")
    pickle.dump(objs, f)
    f.close()