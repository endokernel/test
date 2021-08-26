#!/bin/sh

mkdir -p ../src
mkdir -p ../bin/nocet
mkdir -p ../libs/cet
mkdir -p ../libs/nocet

if ! [ -f "../glibc-nocet/install/lib/libbz2.so.1.0" ] 
then
    cd ../src

    # Build non-cet first
    tar xzvf ../pkg/bzip2-latest.tar.gz

    cd bzip2-1.0.8
    make -f Makefile-libbz2_so -j
    cp *.so.* *.so  ../../glibc-nocet/install/lib
    cp *.so.* *.so ../../libs/nocet
    cd ..
    rm -rf bzip2-1.0.8
fi

if ! [ -f "../glibc-cet/install/lib/libbz2.so.1.0" ] 
then
    cd ../src

    # Build non-cet first
    tar xzvf ../pkg/bzip2-latest.tar.gz

    cd bzip2-1.0.8
    make -f Makefile-libbz2_so CFLAGS="-fpic -fPIC -Wall -Winline -O2 -g -D_FILE_OFFSET_BITS=64 -Wl,-z,shstk -Wl,-z,ibt -fcf-protection -mshstk" -j
    cp *.so.* *.so ../../glibc-cet/install/lib
    cp *.so.* *.so ../../libs/cet
    cd ..
    rm -rf bzip2-1.0.8
fi

