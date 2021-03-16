#/bin/bash

if ! [ -d "../src/intravirt-glibc" ]
then
    mkdir -p ../src
    cd ../src
    git clone git@gitlab.com:fierce-lab/intravirt-glibc.git
    cd ..
    mkdir -p glibc-nocet/build
    cd glibc-nocet/build
    ../../src/intravirt-glibc/configure --prefix=$PWD/../install --with-tls --without-selinux --disable-test --disable-nscd --disable-sanity-checks --disable-werror "CFLAGS=-gdwarf-2 -g3 -O2 -U_FORTIFY_SOURCE -Wno-unused_Value"
    make -j
    make install -j

    cd ../..
    mkdir -p glibc-cet/build
    cd glibc-cet/build
    ../../src/intravirt-glibc/configure --prefix=$PWD/../install --with-tls --without-selinux --disable-test --disable-nscd --disable-sanity-checks --disable-werror --enable-cet=permissive "CFLAGS=-gdwarf-2 -g3 -O2 -U_FORTIFY_SOURCE -Wno-unused-value"
    make -j
    make install -j

    cd ../../script
fi