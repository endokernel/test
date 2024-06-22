#!/bin/bash
./glibc.sh
source ./export.sh

cd ../src
rm -rf endokernel-paper-ver
git clone https://github.com/endokernel/endokernel-paper-ver/
cd endokernel-paper-ver/src/libintravirt
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

mkdir -p dispatch_eiv
cd dispatch_eiv
cmake ../src/endokernel-paper-ver/src/libintravirt -DCFI=NEXPOLINE -DRSYSCALL=DISPATCH -DVDSO=ON -DMT=ON -DRANDOM=OFF -DAPPPERF=OFF -DSYSCALLFILTER=ON 
make -j

cd ../script
