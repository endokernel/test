#!/bin/sh
./glibc.sh

mkdir -p ../libs/cet
mkdir -p ../libs/nocet

mkdir -p ../src

if ! [ -f "../glibc-nocet/install/lib/libz.so.1" ] 
then
    cd ../src

    # Build non-cet first
    tar xzvf ../pkg/zlib-1.2.11.tar.gz

    cd zlib-1.2.11
    ./configure
    make -j
    cp *.so.* *.so ../../glibc-nocet/install/lib
    cp *.so.* *.so ../../libs/nocet
    cd ..
    rm -rf zlib-1.2.11
fi

if ! [ -f "../glibc-cet/install/lib/libz.so.1" ] 
then
    # Build CET version
    tar xzvf ../pkg/zlib-1.2.11.tar.gz

    cd zlib-1.2.11
    ./configure
    make CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" SFLAGS="-fcf-protection -mshstk" -j
    cp *.so.* *.so ../../glibc-cet/install/lib
    cp *.so.* *.so ../../libs/cet
    cd ..
    rm -rf zlib-1.2.11
fi
