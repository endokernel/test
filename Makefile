ARCH := $(uname -r)
FLAGS := $(cat /proc/cpuinfo)

ifneq (,$(findstring cet,$(ARCH)))
    CET := 1
	DEPS := glibc-nocet/done glibc-cet/done
	PREBUILT := prebuilt/glibc-nocet.zip prebuilt/glibc-cet.zip
else
    CET := 0
	DEPS := glibc-nocet/done
	PREBUILT := prebuilt/glibc-nocet.zip prebuilt/glibc-cet.zip
endif

PKU := 1 # must have pku

info:
	@echo "CET=${CET}"
	@echo "PKU=${PKU}"

glibc-nocet/done: prebuilt/glibc-nocet.zip
	unzip $< -d .
	mv glibc-nocet glibc-nocet-t
	mkdir glibc-nocet
	mv glibc-nocet-t glibc-nocet/install

glibc-cet/done: prebuilt/glibc-cet.zip
	unzip $< -d .
	mv glibc-cet glibc-cet-t
	mkdir glibc-cet
	mv glibc-cet-t glibc-cet/install


intravirt/done: prebuilt/intravirt.zip
	unzip $< -d .
	mv ./build ./intravirt
	touch $@

unpack: $(DEPS) intravirt/done

image: 
	docker build -t intravirt-env -f Dockerfile \
		--build-arg CET=${CET} --build-arg PKU=${PKU} \
		--build-arg PREBUILT="${PREBUILT}" \
		.

build-prog: unpack
	cd ./script && ./setup.sh
	touch build-prog

test: 
	docker run --runtime runq --rm --security-opt=seccomp:unconfined \
		intravirt-env make runtest

shell: 
	docker run --runtime runq -ti --rm --security-opt=seccomp:unconfined intravirt-env

runtest:
