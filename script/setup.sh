#/bin/bash
mkdir -p ../result
./glibc.sh
./iv.sh
./lmbench_nocet.sh
./lmbench_cet.sh
./sysbench.sh
./lighttpd.sh
./nginx.sh
./sqlite.sh
./zip.sh
./iv-openssl.sh
./iv-nginx.sh
./curl.sh

