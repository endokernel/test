#!/bin/sh
./nginx.sh

mkdir -p ../src
cd ../src

# Non-CET version
if ! [ -f "../openssl-install/lib/libssl.so" ]
then
    mkdir -p ../openssl-install
    #cp -r ../glibc-nocet/install/lib ../safe-sand/nocet/glibc/install
    git clone git@gitlab.com:fierce-lab/iv-openssl.git --branch libisoV2_111
    mkdir -p openssl-build
    cd openssl-build
    ../iv-openssl/Configure --prefix=$PWD/../../openssl-install --openssldir=$PWD/../../openssl-install/etc/ssl --libdir=lib no-ocb shared linux-x86_64 no-asm "-g $CPPFLAGS $CFLAGS $LDFLAGS"
    make -j depend
    make -j
    make -j install
    #cd ..
    rm -rf openssl-build iv-openssl


fi
: '
# CET version
if ! [ -f "../openssl-cet-install/cet/libssl.so" ]
then
    mkdir -p ../openssl-cet-install
    #cp -r ../glibc-cet/install/lib ../safe-sand/cet/glibc/install
    git clone git@gitlab.com:fierce-lab/iv-openssl.git --branch libisoV2_111
    mkdir -p openssl-build
    cd openssl-build
    ../iv-openssl/Configure --prefix=$PWD/../openssl-cet-install --openssldir=$PWD/../../openssl-cet-install/etc/ssl --libdir=lib no-ocb shared linux-x86_64 no-asm "-Wa,--noexecstack -fcf-protection -mshstk -g $CPPFLAGS $CFLAGS $LDFLAGS"
    make -j depend
    make -j 
    make -j install
    # cd ..
    rm -rf openssl-build iv-openssl
fi
'