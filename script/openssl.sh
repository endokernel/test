#!/bin/sh

mkdir -p ../src
mkdir -p ../libs/cet
mkdir -p ../libs/nocet

cd ../src

if ! [ -f "../glibc-nocet/install/lib/libssl.so.1.1" ]
then 
    tar xzvf ../pkg/openssl-1.1.1i.tar.gz
    cd openssl-1.1.1i
    ./Configure shared linux-x86_64
    make -j
    cp *.so.* *.so ../../glibc-nocet/install/lib
    cp *.so.* *.so ../../libs/nocet
    cp *.so.* *.so ../../glibc-cet/install/lib	# Should be removed if OpenSSL supports CET
    cp *.so.* *.so ../../libs/cet	# Should be removed if OpenSSL supports CET
    cd ..
    rm -rf openssl-1.1.1i
fi

# OpenSSL does not support CET. Assembly code of OpenSSL does not have endbranch instruction.
# We use non-cet version at the moment.

: '
# Build for CET version
if ! [ -f "../glibc-cet/install/lib/libssl.so.1.1" ]
then
    tar xzvf ../pkg/openssl-1.1.1i.tar.gz
    cd openssl-1.1.1i
    ./Configure shared linux-x86_64 CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp *.so.* *.so ../../glibc-cet/install/lib
    cp *.so.* *.so ../../libs/cet
    cd ..
    rm -rf openssl-1.1.1i
fi

'