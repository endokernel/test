#!/bin/sh

if ! [ -d "../www" ]
then
    mkdir -p ../www/logs
    cd ../www
    touch 0k.bin
    dd if=/dev/urandom of=1k.bin bs=1024 count=1
    dd if=/dev/urandom of=2k.bin bs=1024 count=2
    dd if=/dev/urandom of=4k.bin bs=1024 count=4
    dd if=/dev/urandom of=8k.bin bs=1024 count=8
    dd if=/dev/urandom of=16k.bin bs=1024 count=16
    dd if=/dev/urandom of=32k.bin bs=1024 count=32
    dd if=/dev/urandom of=64k.bin bs=1024 count=64
    dd if=/dev/urandom of=128k.bin bs=1024 count=128
    dd if=/dev/urandom of=256k.bin bs=1024 count=256
    dd if=/dev/urandom of=512k.bin bs=1024 count=512
    dd if=/dev/urandom of=1024k.bin bs=1024 count=1024
    dd if=/dev/urandom of=1g.bin bs=1024 count=1048576
    echo "<html><body>It works!<p></body></html>" > index.html
fi
