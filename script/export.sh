export ABSOLUTE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo $ABSOLUTE_PATH
export GLIBCNOCET=$ABSOLUTE_PATH/../glibc-nocet/install
export GLIBCCET=$ABSOLUTE_PATH/../glibc-cet/install
#export ltemporal=/home/dell/Projects/intravirt-next/intravirt-src/src/libtemporal/build
#export ivsrc=/home/dell/Projects/intravirt-next/intravirt-src/