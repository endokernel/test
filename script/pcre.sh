#!/bin/sh
./glibc.sh

mkdir -p ../src
mkdir -p ../libs/cet
mkdir -p ../libs/nocet

cd ../src

# Build non-cet first
if ! [ -f "../glibc-nocet/install/lib/libpcre.so.1" ]
then
    tar xzvf ../pkg/pcre-8.44.tar.gz
    cd pcre-8.44
    ./configure
    make -j
    cp .libs/*.so.* .libs/*.so ../../glibc-nocet/install/lib
    cp .libs/*.so.* .libs/*.so ../../libs/nocet
    cd ..
    rm -rf pcre-8.44
fi

if ! [ -f "../glibc-cet/install/lib/libpcre.so.1" ]
then
    # Build for CET version
    tar xzvf ../pkg/pcre-8.44.tar.gz
    cd pcre-8.44
    ./configure CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp .libs/*.so.* .libs/*.so ../../glibc-cet/install/lib
    cp .libs/*.so.* .libs/*.so ../../libs/cet
    cd ..
    rm -rf pcre-8.44
fi
