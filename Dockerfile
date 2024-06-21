FROM ubuntu:20.10

ARG CET=0
ARG PKU=1

ENV CET ${CET}
ENV PKU ${PKU}

WORKDIR /intravirt

RUN sed -i 's|archive.ubuntu.com|old-releases.ubuntu.com|g' /etc/apt/sources.list \
    && sed -i 's|security.ubuntu.com|old-releases.ubuntu.com|g' /etc/apt/sources.list \
    && apt-get update

RUN apt-get update -qq && apt-get install -y -qq nano gdb strace unzip pkg-config build-essential git cmake libncurses-dev gawk flex bison openssl libssl-dev dkms libelf-dev libudev-dev libpci-dev libiberty-dev autoconf libdwarf-dev libdw-dev libaio-dev libpcre3-dev libtool uuid-dev libblkid-dev apache2-utils automake autoconf libtool-bin wget dwarves

RUN ls -a

COPY ./pkg /intravirt/pkg
COPY ./script /intravirt/script
COPY ./Makefile /intravirt/Makefile
COPY ./prebuilt /intravirt/prebuilt
RUN make build-prog
COPY ./conf /intravirt/conf
COPY ./testcases /intravirt/testcases
RUN sudo apt install -y python curl apache2-utils psmisc
