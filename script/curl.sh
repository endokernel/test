#!/bin/sh
./glibc.sh
./lighttpd.sh
./nginx.sh

mkdir -p ../src
mkdir -p ../libs/cet
mkdir -p ../libs/nocet
mkdir -p ../bin/cet
mkdir -p ../bin/nocet

cd ../src

# Build non-cet first
if ! [ -f "../bin/nocet/curl" ]
then
    tar xzvf ../pkg/curl-7.75.0.tar.gz
    cd curl-7.75.0
    ./configure --disable-ftp --disable-ldap --disable-rtsp --disable-proxy --disable-dict --disable-telnet --disable-tftp --disable-pop3 --disable-imap --disable-smb --disable-smtp --disable-gopher --disable-mqtt --disable-manual --disable-libcurl-option --disable-ipv6 --disable-sspi --disable-tls-srp --disable-htts --disable-alt-svc --without-brotli --without-zstd --without-gnutls --without-nss --without-libpsl --without-libmetalink --without-librtmp --without-libind2 --without-libidn --without-nghttp2 --without-ngtcp2 --without-nghttp3 --without-quiche --without-hyper --without-zsh-functions-dir
    make -j
    cp src/.libs/curl ../../bin/nocet
    cp lib/.libs/*.so.* lib/.libs/*.so* ../../libs/nocet
    cp lib/.libs/*.so.* lib/.libs/*.so* ../../glibc-nocet/install/lib
    cd ..
    rm -rf curl-7.75.0
fi

# Build cet
if ! [ -f "../bin/cet/curl" ]
then
    tar xzvf ../pkg/curl-7.75.0.tar.gz
    cd curl-7.75.0
    ./configure --disable-ftp --disable-ldap --disable-rtsp --disable-proxy --disable-dict --disable-telnet --disable-tftp --disable-pop3 --disable-imap --disable-smb --disable-smtp --disable-gopher --disable-mqtt --disable-manual --disable-libcurl-option --disable-ipv6 --disable-sspi --disable-tls-srp --disable-htts --disable-alt-svc --without-brotli --without-zstd --without-gnutls --without-nss --without-libpsl --without-libmetalink --without-librtmp --without-libind2 --without-libidn --without-nghttp2 --without-ngtcp2 --without-nghttp3 --without-quiche --without-hyper --without-zsh-functions-dir CPPFLAGS="-fcf-protection -mshstk" LDFLAGS="-Wl,-z,shstk -Wl,-z,ibt"
    make -j
    cp src/.libs/curl ../../bin/cet
    cp lib/.libs/*.so.* lib/.libs/*.so* ../../libs/cet
    cp lib/.libs/*.so.* lib/.libs/*.so* ../../glibc-cet/install/lib
    cd ..
    rm -rf curl-7.75.0
fi
