#!/bin/sh

mkdir -p ../src
cd ../src

# Non-CET version
if ! [ -d "../zlib/nocet" ]
then
    mkdir -p ../zlib/nocet/glibc/install
    cp -r ../glibc-nocet/install/lib ../zlib/nocet/glibc/install
    tar xzvf ../pkg/zlib-1.2.11.tar.gz
    cd zlib-1.2.11
    patch < ../../pkg/zlib.patch
    ./configure
    make -j
    cp *.so.* *.so* ../../zlib/nocet/glibc/install/lib
    cd ..
    rm -rf zlib-1.2.11
fi

if ! [ -f "../bin/nocet/zlib_test" ]
then
    gcc -o ../bin/nocet/zlib_test ../pkg/zlib-test.c -ldl -lz
fi



# CET version
if ! [ -d "../zlib/cet" ]
then
    mkdir -p ../zlib/cet/glibc/install
    cp -r ../glibc-cet/install/lib ../zlib/cet/glibc/install
    tar xzvf ../pkg/zlib-1.2.11.tar.gz
    cd zlib-1.2.11
    patch < ../../pkg/zlib.patch
    ./configure
    make CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" SFLAGS="-fcf-protection -mshstk -fPIC" -j
    cp *.so.* *.so* ../../zlib/cet/glibc/install/lib
    cd ..
    rm -rf zlib-1.2.11
fi

if ! [ -f "../bin/cet/zlib_test" ]
then
    gcc -o ../bin/cet/zlib_test ../pkg/zlib-test.c -fcf-protection -mshstk -ldl -lz
fi

