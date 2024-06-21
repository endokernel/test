#!/bin/bash
./libxcrypt.sh
./pcre3.sh
./openssl.sh
./zlib.sh
source ./export.sh 
# Build non-cet first
if ! [ -f "../safe-sand/nocet/nginx" ]
then
    mkdir -p ../src
    mkdir -p ../safe-sand/nocet
    cd ../src
    git clone git@gitlab.com:fierce-lab/iv-nginx.git
    cd iv-nginx
    git checkout rc2
    export GLIBC=$GLIBCNOCET
    export ltemporal=$GLIBC/lib/ 
    export ivsrc=$ABSOLUTE_PATH/../src/intravirt-src/
    ./configure --with-http_ssl_module
    make -j
    cp objs/nginx ../../safe-sand/nocet
    cd ..
    rm -rf iv-nginx
fi
: '
# Build non-cet first
if ! [ -f "../safe-sand/cet/nginx" ]
then
    mkdir -p ../src
    mkdir -p ../safe-sand/cet
    cd ../src
    git clone git@gitlab.com:fierce-lab/iv-nginx.git
    cd iv-nginx
    git checkout rc2
    export GLIBC=$GLIBCCET
    export ltemporal=$GLIBC/lib/ 
    export ivsrc=$ABSOLUTE_PATH/../src/intravirt-src/
    ./configure --with-http_ssl_module --with-cc-opt="-fno-stack-protector -fno-jump-tables -fcf-protection -mshstk" --with-ld-opt="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp objs/nginx ../../safe-sand/cet
    cd ..
    rm -rf iv-nginx
fi
'
# Create config file
if ! [ -f "../conf/nginx.conf" ]
then
    cd ../conf
    cat ./nginx.conf_original | sed 's?PUT_YOUR_CONF_HERE?'`pwd`'?' > ../conf/nginx.conf
fi