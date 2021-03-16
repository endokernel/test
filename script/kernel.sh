#!/bin/sh

mkdir -p ../src
cd ../src

# Build the kernel
git clone git@gitlab.com:fierce-lab/intravirt-kern.git
cd intravirt-kern
git checkout netcetapi-5.9.8
git pull
make mrproper
cp ../../conf/config-5.9.8-cet .config
yes '' | make oldconfig
make clean
make -j $(getconf _NPROCESSORS_ONLN) deb-pkg LOCALVERSION=-cet

