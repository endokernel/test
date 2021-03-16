#!/bin/sh
./glibc.sh

mkdir -p ../src
mkdir -p ../libs/nocet
mkdir -p ../bin/nocet

cd ../src

if ! [ -f "../glibc-nocet/install/lib/libkeyutils.so.1.10" ]
then
    tar xzvf ../pkg/keyutils-1.6.3.tar.gz
    cd keyutils-1.6.3
    make -j
    cp *.so.* *.so ../../glibc-nocet/install/lib
    cp *.so.* *.so ../../libs/nocet
    cd ..
    rm -rf keyutils-1.6.3
fi

if ! [ -f "../glibc-nocet/install/lib/libe2p.so.2.3" ]
then
    tar xzvf ../pkg/e2fsprogs-1.46.0.tar.gz
    cd e2fsprogs-1.46.0
    ./configure --enable-elf-shlibs --disable-libblkid --disable-libuuid --disable-uuidd --disable-fsck
    make -j
    cp lib/*.so.* lib/*.so ../../glibc-nocet/install/lib
    cp lib/*.so.* lib/*.so ../../libs-nocet
    cd ..
    rm -rf e2fsprogs-1.46.0
fi

if ! [ -f "../glibc-nocet/install/lib/libkrb5.so.3.3" ]
then
    tar xzvf ../pkg/krb5-1.18.3.tar.gz
    cd krb5-1.18.3/src
    ./configure
    make -j
    cp lib/*.so.* lib/*.so ../../../glibc-nocet/install/lib
    cp lib/*.so.* lib/*.so ../../../libs/nocet
    cd ../..
    rm -rf krb5-1.18.3
fi

if ! [ -f "../glibc-nocet/install/lib/libtirpc.so.3.0.0" ]
then
    tar xjvf ../pkg/libtirpc-1.3.1.tar.bz2
    cd libtirpc-1.3.1
    ./configure --disable-static --disable-gssapi
    make -j
    cp src/.libs/*.so.* src/.libs/*.so ../../glibc-nocet/install/lib
    cp src/.libs/*.so.* src/.libs/*.so ../../libs/nocet
    cd ..
    rm -rf libtirpc-1.3.1
fi

if ! [ -f "../bin/nocet/lat_syscall" ]
then
    tar xzvf ../pkg/lmbench-2.5.tar.gz
    cd lmbench-2.5
    make CFLAGS="-I/usr/include/tirpc" LDLIBS="-ltirpc" -j

    mkdir -p ../../bin/cet
    cp bin/x86_64-linux-gnu/lat_syscall bin/x86_64-linux-gnu/lat_sig bin/x86_64-linux-gnu/lat_mmap ../../bin/nocet
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/64k

    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(1*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/1k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(2*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/2k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(4*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/4k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(8*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/8k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(16*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/16k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(32*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/32k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(128*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/128k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(256*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/256k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(512*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/512k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(1024*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/1024k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(2048*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/2048k
    make clean
    make CFLAGS="-I/usr/include/tirpc -DXFERSIZE=\(4096*1024\)" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/nocet/4096k

    cd ..
    rm -rf lmbench-2.5
fi
