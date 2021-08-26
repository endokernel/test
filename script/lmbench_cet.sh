#!/bin/sh

mkdir -p ../libs/cet
mkdir -p ../bin/cet

mkdir -p ../src
cd ../src


if ! [ -f "../glibc-cet/install/lib/libkeyutils.so.1.10" ]
then
    tar xzvf ../pkg/keyutils-1.6.3.tar.gz
    cd keyutils-1.6.3
    make CFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" -j
    cp *.so.* *.so ../../glibc-cet/install/lib
    cp *.so.* *.so ../../libs/cet
    cd ..
    rm -rf keyutils-1.6.3
fi

if ! [ -f "../glibc-cet/install/lib/libe2p.so.2.3" ]
then
    tar xzvf ../pkg/e2fsprogs-1.46.0.tar.gz
    cd e2fsprogs-1.46.0
    ./configure --enable-elf-shlibs --disable-libblkid --disable-libuuid --disable-uuidd --disable-fsck CFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp lib/*.so.* lib/*.so ../../glibc-cet/install/lib
    cp lib/*.so.* lib/*.so ../../libc/cet
    cd ..
    rm -rf e2fsprogs-1.46.0
fi

if ! [ -f "../glibc-cet/install/lib/libkrb5.so.3.3" ]
then
    tar xzvf ../pkg/krb5-1.18.3.tar.gz
    cd krb5-1.18.3/src
    ./configure CFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp lib/*.so.* lib/*.so ../../../glibc-cet/install/lib
    cp lib/*.so.* lib/*.so ../../../libs/cet
    cd ../..
    rm -rf krb5-1.18.3
fi

if ! [ -f "../glibc-cet/install/lib/libtirpc.so.3.0.0" ]
then
    tar xjvf ../pkg/libtirpc-1.3.1.tar.bz2
    cd libtirpc-1.3.1
    ./configure --disable-static --disable-gssapi CFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp src/.libs/*.so.* src/.libs/*.so ../../glibc-cet/install/lib
    cp src/.libs/*.so.* src/.libs/*.so ../../libs/cet
    cd ..
    rm -rf libtirpc-1.3.1
fi

if ! [ -f "../bin/cet/lat_syscall" ]
then
    tar xzvf ../pkg/lmbench-2.5.tar.gz
    cd lmbench-2.5
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j

    mkdir -p ../../bin/cet
    cp bin/x86_64-linux-gnu/lat_syscall bin/x86_64-linux-gnu/lat_sig bin/x86_64-linux-gnu/lat_mmap ../../bin/cet
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/64k

    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(1*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/1k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(2*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/2k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(4*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/4k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(8*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/8k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(16*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/16k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(32*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/32k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(128*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/128k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(256*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/256k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(512*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/512k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(1024*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/1024k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(2048*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/2048k
    make clean
    make CFLAGS="-I/usr/include/tirpc -fcf-protection -mshstk -DXFERSIZE=\(4096*1024\)" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt" LDLIBS="-ltirpc" -j
    cp bin/x86_64-linux-gnu/bw_file_rd ../../bin/cet/4096k

    cd ..
    rm -rf lmbench-2.5
fi
