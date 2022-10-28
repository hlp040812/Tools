#!/bin/bash
#########################################################################
# File Name: pdb2arc.sh
# Author: wdhu@219.220.210.138
# Created Time: Tue 26 Jul 2022 11:50:52 AM CST
#########################################################################
echo -ne "!BIOSYM archive 3\nPBC=ON\n"
awk '{if($1 == "REMARK")
        {printf"Auto Generated CAR File\n!DATE %s\n",strftime("%a %b %e %H:%M:%S  %Y")}
    else if($1 == "CRYST1")
        {printf"PBC   %.5f  %.5f  %.5f  %.5f  %.5f  %.5f (P1)\n", $2,$3,$4,$5,$6,$7}
    else if($1 == "ATOM")
        {printf"%-5s %14.9f %14.9f %14.9f XXXX 1       xx     %-2s 0.0000\n",$3,$4,$5,$6,$9}
    else if($1 == "END")
        {printf"end\nend\n"}
    }' $1
