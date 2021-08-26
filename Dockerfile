FROM ubuntu:20.10

ARG CET=0
ARG PKU=1

ENV CET ${CET}
ENV PKU ${PKU}

WORKDIR /intravirt

RUN apt-get update -qq && apt-get install -y -qq nano gdb strace unzip pkg-config build-essential git cmake libncurses-dev gawk flex bison openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf libdwarf-dev libdw-dev libaio-dev libpcre3-dev libtool uuid-dev libblkid-dev apache2-utils automake autoconf libtool-bin wget dwarves

RUN ls -a

COPY ./pkg /intravirt/pkg
COPY ./script /intravirt/script
COPY ./testcases /intravirt/testcases
COPY ./Makefile /intravirt/Makefile
COPY ./prebuilt /intravirt/prebuilt
RUN make build-prog
