# IntraVirt Full Test Suite
This suite includes IntraVirt source code, all the test code and the dependent libraries.
## Requirement
### Hardware
- CPU: Intel TigerLake architecture with CET(TM)  and MPK(TM) enabled
- RAM: 8GB and more
- Storage: At least 50Gbytes free space
- Internet access
### Software
- Operating System: Ubuntu 20.10 X86_64
- IntraVirt gitlab access

## Directory structure
### Before build
```
/
+-+- conf               # All the configuration files
| +--- ssl              # Self signed test certificates and keys for OpenSSL
+--- pkg                # All the dependent pkg source codes
+--- script             # Shell scripts to build the test suites
+-+- testcases          # Test case scripts
  +--- inactive         # Obsolete test case scripts
```
### After build
- Not all the subdirectories are described here.
```
/
+-+- bin                # Binary executables
| +--- cet              # CET enabled binary
| +--- nocet            # CET disabled binary
+-+- conf               # All the configuration files
| +--- ssl              # Self signed test certificates and keys for OpenSSL
+--- dispatch_cet       # IntraVirt binary for user-dispatch and CET
+--- dispatch_eiv       # IntraVirt binary for user-dispatch and EIV
+-+- glibc-cet          # CET enabled GLIBC for IntraVirt
| +--- build            # Glibc build directory
| +-+- install          # Glibc install directory
|   +--- lib            # All the dependent libraries with CET. IntraVirt does not support ld.so.conf
+-+- glibc-nocet          # CET disabled GLIBC for IntraVirt
| +--- build            # Glibc build directory
| +-+- install          # Glibc install directory
|   +--- lib            # All the dependent libraries without CET. IntraVirt does not support ld.so.conf
+-+- libs               # Additional storage for dependent libraries
| +--- cet              # All the libraries with CET
| +--- nocet            # All the libraries without CET
+--- linux-5.9.8        # Linux source tree for testing ZIP
+--- pkg                # All the dependent pkg source codes
+--- queen              # IntraVirt binary for Seccomp and EIV
+--- random1            # IntraVirt binary for Seccomp and RIV with freq 1
+--- random2            # IntraVirt binary for Seccomp and RIV with freq 2
+--- random4            # IntraVirt binary for Seccomp and RIV with freq 4
+--- random8            # IntraVirt binary for Seccomp and RIV with freq 8
+--- random16           # IntraVirt binary for Seccomp and RIV with freq 16
+--- random32           # IntraVirt binary for Seccomp and RIV with freq 32
+--- random1024         # IntraVirt binary for Seccomp and RIV with freq 1024
+--- result             # Test result files as CSV format
+-+- safe-sand          # Binary for safebox and sandbox
| +--- cet              # CET enabled safe-sandbox binaries
| +--- nocet            # CET disabled safe-sandbox binaries
+--- script             # Shell scripts to build the test suites
+--- seccomp_cet        # IntraVirt binary for Seccomp and CET
+-+- src                # Source code directory
| +--- intravirt-glibc  # Source for IntraVirt enabled GLIBC
| +--- intravirt-kernel # Source for IntraVirt kernel with CET patches and user-dispatch patches
| +--- intravirt-src    # Source for IntraVirt
+-+- testcases          # Test case scripts
| +--- inactive         # Obsolete test case scripts
+--- www                # Web server root directory

```

## Build
### Installing Dependencies
You need to install libraries which are required to build the tools.
```
$ cd script
$ ./dep.sh              # This requires root password
```
### Kernel
IntraVirt requires CET enabled kernel which is maintained by IntraVirt research group.
Executing the script will do everything for you, but you will need to install the deb packages.

The kernel is originally forked from Arch Linux source tree, but it works fine in Ubuntu 20.10.

**_NOTE:_** If your system does not support CET, you don't need this step.
```
$ cd script
$ ./kernel.sh           # This will take a while
$ cd ../src
$ sudo dpkg -i linux-image-5.9.8-arch1-cet_5.9.8-arch1-cet-1_amd64.deb linux-headers-5.9.8-arch1-cet_5.9.8-arch1-cet-1_amd64.deb
$ sudo grub-mkconfig -o /boot/grub/grub.cfg
$ reboot
```

## IntraVirt and Test tools
Since everything is prepared, you can simply build all the tools by simply executing a script.
```
$ cd script
$ ./setup.sh        # This will take a while
```

## Prepare
You can adjust test scope, tools, and repetition and some others by modifying `testcases/variable.py`
### Scope
You need to comment out some of the elements in `iv_nocet_paths` and `iv_cet_paths` to skip the scope.
For example, the setup below does not run the test for random2, random4, random8, random32, and random1024.
```
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
```
### Repetition
You can modify the integer value for the variable `tries`.

### Environment
We recommend you to disable any performance features in the bios setup and disable windowing system and network before starting the measurement.

## Run

### lmbench
```
$ cd testcases
$ python3 lmbench.py        # This will take a while
```
The result CSV files are stored in `result` directory. File names are `lmbench_[setupname].csv`

### file bandwidth
```
$ cd testcases
$ python3 file_bw.py        # This will take a while
```
The result CSV files are stored in `result` directory. File names are `file_bw_[setupname].csv`

### sysbench
```
$ cd testcases
$ python3 sysbench.py       # This will take a while
```
The script will creates test files. You could remove them after the test.

The result CSV files are stored in `result` directory. File names are `sysbench_[setupname].csv`

### sqlite
```
$ cd testcases
$ python3 sqlite.py         # This will take a while
```
The result CSV files are stored in `result` directory. File names are `sqlite_[setupname].csv`

### lighttpd
```
$ cd testcases
$ python3 lighttpd.py       # This will take a while
```
The result CSV files are stored in `result` directory. File names are `lighttpd_[setupname].csv`

### nginx
```
$ cd testcases
$ python3 nginx.py          # This will take a while
```
The result CSV files are stored in `result` directory. File names are `nginx_[setupname].csv`


### zip
```
$ cd testcases
$ python3 sqlite.py         # This will take a while
```
The result CSV file is stored in `result` directory. File names are `zip.csv`

### curl
```
$ cd testcases
$ python3 curl.py           # This will take a while
```
The result CSV file is stored in `result` directory. File names are `curl.csv`

### sandbox, safebox
```
$ cd testcases
$ python3 safe_sand.py	    # This will take a while
```
The result CSV file is stored in `result` directory. File names are `safesand_[setupname].csv`

## Cleaning up
You can simply run a clean up script. It will remove all the produced files and restore back to the original.
```
$ cd script
$ ./cleanup.sh
```

## TODO:
- Safe-sandbox test run script is missing.
