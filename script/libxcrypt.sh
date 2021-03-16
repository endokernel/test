#!/bin/sh
./glibc.sh

mkdir -p ../src
mkdir -p ../libs/cet
mkdir -p ../libs/nocet

cd ../src

# Build non-cet first
if ! [ -f "../libs/nocet/libcrypt.so.1" ]
then
    tar xzvf ../pkg/libxcrypt-4.4.16.tar.gz
    cd libxcrypt-4.4.16
    ./autogen.sh
    ./configure
    make -j
    # Remove original one from glibc
    rm ../../glibc-nocet/install/lib/libcrypt.so*
    cp .libs/*.so.* .libs/*.so ../../glibc-nocet/install/lib
    cp .libs/*.so.* .libs/*.so ../../libs/nocet
    cd ..
    rm -rf libxcrypt-4.4.16
fi

# Build for CET version
if ! [ -f "../libs/cet/libcrypt.so.1" ]
then
    tar xzvf ../pkg/libxcrypt-4.4.16.tar.gz
    cd libxcrypt-4.4.16
    ./autogen.sh
    ./configure CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    # Remove original one from glibc
    rm ../../glibc-cet/install/lib/libcrypt.so*
    cp .libs/*.so.* .libs/*.so ../../glibc-cet/install/lib
    cp .libs/*.so.* .libs/*.so ../../libs/cet
    cd ..
    rm -rf libxcrypt-4.4.16
fi
