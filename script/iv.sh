#!/bin/bash
./glibc.sh
source ./export.sh

cd ../src
#rm -rf intravirt-src
#git clone git@gitlab.com:fierce-lab/intravirt-src.git
cd intravirt-src/src/libintravirt
#git checkout rc7
#cat printf.c | sed 's/int quiet = 0;/int quiet = 1;/' > printf.1
#mv printf.1 printf.c

# build libtemporal
pushd ../libtemporal
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/ ..
make -j
DESTDIR=$GLIBCCET make install -j
DESTDIR=$GLIBCNOCET make install -j
popd

cd ../../../../
mkdir -p random1
cd random1
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 1/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p random2
cd random2
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 2/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p random4
cd random4
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 4/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p random8
cd random8
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 8/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p random16
cd random16
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 16/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p random32
cd random32
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 32/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p random1024
cd random1024
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON -DRANDOM=ON
cat ../src/intravirt-src/src/libintravirt/syscall_trap.S | sed -r 's/#define RFREQ [0-9]+/#define RFREQ 1024/' > syscall_trap.S1
cp syscall_trap.S1 ../src/intravirt-src/src/libintravirt/syscall_trap.S
make -j

cd ..
mkdir -p queen
cd queen
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=SECCOMP -DMT=ON
make -j

cd ..
mkdir -p seccomp_cet
cd seccomp_cet
cmake ../src/intravirt-src/src/libintravirt -DCFI=CET -DRSYSCALL=SECCOMP -DMT=ON
make -j

cd ..
mkdir -p dispatch_eiv
cd dispatch_eiv
cmake ../src/intravirt-src/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=DISPATCH -DMT=ON
make -j

cd ..
mkdir -p dispatch_cet
cd dispatch_cet
cmake ../src/intravirt-src/src/libintravirt -DCFI=CET -DRSYSCALL=DISPATCH -DMT=ON
make -j

cd ../script
