#/bin/bash
mkdir -p ../result
./lmbench_nocet.sh
if [ "$CET" == "1" ] ; then ./lmbench_cet.sh; fi
./sysbench.sh
./lighttpd.sh
./nginx.sh
./sqlite.sh
./zip.sh
./iv-openssl.sh
./iv-nginx.sh
./curl.sh
./iv-zlib.sh

