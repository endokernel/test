#!/bin/sh
./libxcrypt.sh
./pcre3.sh
./openssl.sh
./zlib.sh

mkdir -p ../bin/cet
mkdir -p ../bin/nocet

# Build non-cet first
if ! [ -f "../bin/nocet/nginx" ]
then
    mkdir -p ../src
    cd ../src
    tar xzvf ../pkg/nginx-1.18.0.tar.gz
    cd nginx-1.18.0
    ./configure --with-http_ssl_module --with-cc-opt="-fno-stack-protector -fno-jump-tables"
    make -j
    cp objs/nginx ../../bin/nocet
    cd ..
    rm -rf nginx-1.18.0
fi
: '
# Build for CET version
if ! [ -f "../bin/cet/nginx" ]
then
    tar xzvf ../pkg/nginx-1.18.0.tar.gz
    cd nginx-1.18.0
    ./configure --with-http_ssl_module --with-cc-opt="-fno-stack-protector -fno-jump-tables -fcf-protection -mshstk" --with-ld-opt="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp objs/nginx ../../bin/cet
    cd ..
    rm -rf nginx-1.18.0
fi
'
# Create config file
if ! [ -f "../conf/nginx.conf" ]
then
    cd ../conf
    cat ./nginx.conf_original | sed 's?PUT_YOUR_CONF_HERE?'`pwd`'?' > ../conf/nginx.conf
fi
