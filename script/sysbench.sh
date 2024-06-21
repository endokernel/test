#!/bin/sh

mkdir -p ../src
mkdir -p ../libs/cet
mkdir -p ../libs/nocet
mkdir -p ../bin/cet
mkdir -p ../bin/nocet
cd ../src

# Build non-cet first
if ! [ -f "../glibc-nocet/install/lib/libaio.so.1" ]
then
    tar xJvf ../pkg/libaio_0.3.112.orig.tar.xz
    cd libaio-0.3.112
    make -j
    cp src/libaio.so.1.0.1 ../../glibc-nocet/install/lib/libaio.so.1
    cp src/libaio.so.1.0.1 ../../libs/nocet/libaio.so.1
    cd ..
    rm -rf libaio-0.3.112
fi

########### We need to build gcc for libgcc_s.so in future
cp /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 ../glibc-nocet/install/lib

if ! [ -f "../bin/nocet/sysbench" ]
then
    tar xzvf ../pkg/sysbench-1.0.20.tar.gz
    cd sysbench-1.0.20
    ./autogen.sh
    ./configure --without-mysql
    make -j
    cp src/sysbench ../../bin/nocet/
    cd ..
    rm -rf sysbench-1.0.20
fi

: '
# Build CET version
if ! [ -f "../glibc-cet/install/lib/libaio.so.1" ]
then
    tar xJvf ../pkg/libaio_0.3.112.orig.tar.xz
    cd libaio-0.3.112
    make CFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    cp src/libaio.so.1.0.1 ../../glibc-cet/install/lib/libaio.so.1
    cp src/libaio.so.1.0.1 ../../libs/cet/libaio.so.1
    cd ..
    rm -rf libaio-0.3.112
fi

# Default libgcc_s.so.1 is already CET enabled, which is good for us.
cp /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 ../glibc-cet/install/lib
'

if ! [ -f "../bin/cet/sysbench" ]
then
    tar xzvf ../pkg/sysbench-1.0.20.tar.gz
    cd sysbench-1.0.20
    ./autogen.sh
    ./configure --without-mysql
    make -j
    cp src/sysbench ../../bin/cet/
    cd ..
    rm -rf sysbench-1.0.20
fi
