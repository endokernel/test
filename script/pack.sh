#!/bin/bash
./bin/nocet/zip -r /intravirt-env/glibc-nocet.zip ./glibc-nocet/install
./bin/nocet/zip -r /intravirt-env/intravirt.zip ./dispatch_eiv
./bin/nocet/zip -r /intravirt-env/bin.zip ./bin
./bin/nocet/zip -r /intravirt-env/libs.zip ./libs