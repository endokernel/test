#!/bin/sh
./zlib.sh

mkdir -p ../bin/nocet
mkdir -p ../bin/cet

mkdir -p ../src
cd ../src

# Build non-cet first
if ! [ -f "../bin/nocet/sqlite_speedtest" ]
then
    tar xzvf ../pkg/sqlite.tar.gz

    cd sqlite
    ./configure
    make speedtest1 -j
    cp speedtest1 ../../bin/nocet/sqlite_speedtest
    cd ..
    rm -rf sqlite
fi

: '
# Build CET version
if ! [ -f "../bin/cet/sqlite_speedtest" ]
then
    tar xzvf ../pkg/sqlite.tar.gz

    cd sqlite
    ./configure CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make speedtest1 -j
    cp speedtest1 ../../bin/cet/sqlite_speedtest
    cd ..
    rm -rf sqlite
fi
'