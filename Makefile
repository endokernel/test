ARCH := $(uname -r)
FLAGS := $(cat /proc/cpuinfo)
USE_PREBUILT := 1

ifneq (,$(findstring cet,$(ARCH)))
    CET := 1
	DEPS := glibc-nocet/done glibc-cet/done libs/done bin/done
	ifeq ($(USE_PREBUILT),1)
		PREBUILT := prebuilt/glibc-nocet.zip prebuilt/glibc-cet.zip prebuilt/libs.zip prebuilt/bin.zip
	endif
else
    CET := 0
	DEPS := glibc-nocet/done libs/done bin/done
	ifeq ($(USE_PREBUILT),1)
		PREBUILT := prebuilt/glibc-nocet.zip prebuilt/glibc-cet.zip prebuilt/libs.zip prebuilt/bin.zip
	endif
endif

# add dependencies to unpack if PREBUILT is set
ifneq (,$(PREBUILT))
	PREBUILT_DEPS := unpack
else
	PREBUILT_DEPS := iv_stamp
endif

PKU := 1 # must have pku

info:
	@echo "CET=${CET}"
	@echo "PKU=${PKU}"
	

glibc-nocet/done: prebuilt/glibc-nocet.zip
	unzip $< -d .
	touch $@

glibc-cet/done: prebuilt/glibc-cet.zip
	unzip $< -d .
	touch $@

libs/done: prebuilt/libs.zip
	unzip $< -d .
	touch $@

bin/done: prebuilt/bin.zip
	unzip $< -d .
	touch $@

intravirt/done: prebuilt/intravirt.zip
	unzip $< -d .
	mkdir -p intravirt
	touch $@

pack:
	docker run --rm --security-opt=seccomp:unconfined \
		-v $(shell pwd):/intravirt-env \
		intravirt-env /intravirt-env/script/pack.sh

unpack: $(DEPS) intravirt/done

image: 
	docker build -t intravirt-env -f Dockerfile \
		--build-arg CET=${CET} --build-arg PKU=${PKU} \
		--build-arg PREBUILT="${PREBUILT}" \
		.

iv_stamp:
	cd ./script && ./iv.sh
	touch iv_stamp

build-prog: $(PREBUILT_DEPS)
	cd ./script && ./setup.sh
	touch build-prog

test: 
	docker run --runtime runq --rm --security-opt=seccomp:unconfined \
		intravirt-env make runtest

shell: 
	docker run --runtime runq -ti --rm --security-opt=seccomp:unconfined intravirt-env

runtest:
