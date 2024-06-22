#!/bin/bash

if ! [ -d "../src/glibc" ]
then
    mkdir -p ../src
    cd ../src
    git clone https://github.com/endokernel/glibc
    cd ..
    mkdir -p glibc-nocet/build
    cd glibc-nocet/build
    ../../src/glibc/configure --prefix=$PWD/../install --with-tls --without-selinux --disable-test --disable-nscd --disable-sanity-checks --disable-werror "CFLAGS=-gdwarf-2 -g3 -O2 -U_FORTIFY_SOURCE -Wno-unused_Value"
    make -j
    make install -j

    cd ../../script
fi