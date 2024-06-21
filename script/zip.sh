#!/bin/sh
./libbz2.sh

mkdir -p ../bin/cet
mkdir -p ../bin/nocet

# Build non-cet first
mkdir -p ../src
cd ../src
if ! [ -f "../bin/nocet/zip" ]
    then
    tar xzvf ../pkg/zip30.tar.gz
    cd zip30
    make -f unix/Makefile -j generic_gcc
    cp zip ../../bin/nocet/
    cd ..
    rm -rf zip30
fi
: '
# Build CET version
cd ../script
./libbz2.sh
mkdir -p ../src
mkdir -p ../bin/cet
cd ../src
if ! [ -f "../bin/cet/zip" ]
then
    tar xzvf ../pkg/zip30.tar.gz
    cd zip30
    make -f unix/Makefile LOCAL_ZIP="-fcf-protection -mshstk -Wl,-z,shstk -Wl,-z,ibt" -j generic_gcc
    cp zip ../../bin/cet/
    cd ..
    rm -rf zip30
fi
'
# Prepare test zip file
cd ..
if ! [ -d "linux-5.9.8" ]
then
    wget https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.9.8.tar.gz
    tar xzvf linux-5.9.8.tar.gz
    rm linux-5.9.8.tar.gz
fi
