#!/bin/sh
./libxcrypt.sh
./pcre3.sh
./openssl.sh
./zlib.sh

# Build non-cet first
if ! [ -f "../safe-sand/nocet/nginx" ]
then
    mkdir -p ../src
    mkdir -p ../safe-sand/nocet
    cd ../src
    git clone git@gitlab.com:fierce-lab/iv-nginx.git
    cd iv-nginx
    ./configure --with-http_ssl_module --with-cc-opt="-fno-stack-protector -fno-jump-tables"
    cat objs/Makefile | sed 's?-Werror??' > objs/Makefile1
    mv objs/Makefile1 objs/Makefile
    make -j
    cp objs/nginx ../../safe-sand/nocet
    cd ..
    rm -rf iv-nginx
fi

# Build non-cet first
if ! [ -f "../safe-sand/cet/nginx" ]
then
    mkdir -p ../src
    mkdir -p ../safe-sand/nocet
    cd ../src
    git clone git@gitlab.com:fierce-lab/iv-nginx.git
    cd iv-nginx
    ./configure --with-http_ssl_module --with-cc-opt="-fno-stack-protector -fno-jump-tables -fcf-protection -mshstk" --with-ld-opt="-Wl,-z,shstk -Wl,-z,ibt"
    cat objs/Makefile | sed 's?-Werror??' > objs/Makefile1
    mv objs/Makefile1 objs/Makefile
    make -j
    cp objs/nginx ../../safe-sand/cet
    cd ..
    rm -rf iv-nginx
fi

# Create config file
if ! [ -f "../conf/nginx.conf" ]
then
    cd ../conf
    cat ./nginx.conf_original | sed 's?PUT_YOUR_CONF_HERE?'`pwd`'?' > ../conf/nginx.conf
fi