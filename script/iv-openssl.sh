#!/bin/sh
mkdir -p ../src
cd ../src

# Non-CET version
if ! [ -f "../safe-sand/nocet/libssl.so" ]
then
    mkdir -p ../safe-sand/nocet
    git clone git@gitlab.com:fierce-lab/iv-openssl.git --branch libisoV2_111
    mkdir -p openssl-build
    mkdir -p openssl-install
    cd openssl-build
    ../iv-openssl/Configure --prefix=$PWD/../openssl-install --openssldir=$PWD/../openssl-install/etc/ssl --libdir=lib no-ocb shared linux-x86_64 no-asm "-g $CPPFLAGS $CFLAGS $LDFLAGS"
    make -j depend
    make -j
    cp *.so.* *.so* ../../safe-sand/nocet
    cd ..
    rm -rf openssl-build openssl-install iv-openssl
fi

# CET version
if ! [ -f "../safe-sand/cet/libssl.so" ]
then
    mkdir -p ../safe-sand/cet
    git clone git@gitlab.com:fierce-lab/iv-openssl.git --branch libisoV2_111
    mkdir -p openssl-build
    mkdir -p openssl-install
    cd openssl-build
    ../iv-openssl/Configure --prefix=$PWD/../openssl-install --openssldir=$PWD/../openssl-install/etc/ssl --libdir=lib no-ocb shared linux-x86_64 no-asm "-Wa,--noexecstack -fcf-protection -mshstk -g $CPPFLAGS $CFLAGS $LDFLAGS"
    make -j depend
    make -j
    cp *.so.* *.so* ../../safe-sand/cet
    cd ..
    rm -rf openssl-build openssl-install iv-openssl
fi
