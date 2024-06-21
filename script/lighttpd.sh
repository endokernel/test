#!/bin/sh
./libxcrypt.sh
./pcre3.sh
./www.sh
./openssl.sh

mkdir -p ../bin/cet
mkdir -p ../bin/nocet

mkdir -p ../src
cd ../src

if ! [ -f "../bin/nocet/lighttpd" ] 
then
    mkdir -p ../bin/nocet/lighttpd_module
    # Build non-cet first
    tar xzvf ../pkg/lighttpd-1.4.59.tar.gz
    cd lighttpd-1.4.59
    ./configure --with-openssl
    make -j
    cp src/lighttpd ../../bin/nocet
    cp src/.libs/* ../../bin/nocet/lighttpd_module
    cd ..
    rm -rf lighttpd-1.4.59
fi
: '
# Build for CET version
if ! [ -f "../bin/cet/lighttpd" ] 
then
    mkdir -p ../bin/cet/lighttpd_module
    tar xzvf ../pkg/lighttpd-1.4.59.tar.gz
    cd lighttpd-1.4.59
    ./configure --with-openssl CFLAGS="-fcf-protection -mshstk" CPPFLAGS="-fcf-protection -mshstk" CXXFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp src/lighttpd ../../bin/cet
    cp src/.libs/* ../../bin/cet/lighttpd_module
    cd ..
    rm -rf lighttpd-1.4.59
fi
'
# Create config file
if ! [ -f "../conf/lighttpd.conf" ] 
then
    cd ../www
    cat ../conf/lighttpd.conf_original | sed 's?PUT_YOUR_WWW_HERE?'`pwd`'/?' > ../conf/lighttpd.conf1
    cd ../conf
    cat ../conf/lighttpd.conf1 | sed 's?PUT_YOUR_CONF_HERE?'`pwd`'?' > ../conf/lighttpd.conf
fi
