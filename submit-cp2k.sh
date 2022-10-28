#!/bin/bash

# if input and output are not given, then exit.
if [ $# != 2 ];
then
	echo -e "\033[32m \n\n Example: \033[0m sub-cp2k.sh cp2k.inp cp2k.out & \n "
	echo -e " exit \n"
	exit 0
fi

#echo $1 $2

source /home/luping/cp2k-8.2/tools/toolchain/install/setup
export PATH=$PATH:/home/luping/cp2k-8.2/exe/local/

date > TIMING
cp2k.ssmp $1 > $2 2>&1 
date >> TIMING

