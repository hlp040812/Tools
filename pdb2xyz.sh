#!/bin/bash
#########################################################################
# File Name: pdb2xyz.sh
# Author: wdhu@219.220.210.138
# Created Time: Tue 26 Jul 2022 11:50:52 AM CST
#########################################################################
nend=$(grep -i -n -m 1 END $1 | awk -F ':' '{print $1}')
# echo $nend
natom=$(head -n $nend $1 | grep -i ATOM | wc -l)
# echo $natom

awk '{if($1 == "REMARK")
        {printf"%-s\nE = %.8f  ",'$natom',$NF}
    else if($1 == "CRYST1")
        {printf"PBC %.5f %.5f %.5f %.5f %.5f %.5f \n", $2,$3,$4,$5,$6,$7}
    else if($1 == "ATOM")
        {printf"%-s %14.9f %14.9f %14.9f \n",$9,$4,$5,$6}
    }' $1
