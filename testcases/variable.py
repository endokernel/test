# Intravirt codebases need to measure
iv_nocet_paths = []

iv_nocet_paths.append("baseline")
iv_nocet_paths.append("../random1/")
#iv_nocet_paths.append("../random2/")
#iv_nocet_paths.append("../random4/")
#iv_nocet_paths.append("../random8/")
iv_nocet_paths.append("../random16/")
#iv_nocet_paths.append("../random32/")
#iv_nocet_paths.append("../random1024/")
iv_nocet_paths.append("../queen/")
iv_nocet_paths.append("../dispatch_eiv/")

iv_cet_paths = []
iv_cet_paths.append("../seccomp_cet/")
iv_cet_paths.append("../dispatch_cet/")

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
tries = 1
bindir = "bin"

# Additional variables
cet_glibcpath = "../glibc-cet/install/lib"
glibcpath = "../glibc-nocet/install/lib"

coarse_cet = True
