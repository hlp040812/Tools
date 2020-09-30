#!/usr/bin/python3.6
# coding: utf-8

import sys, os, subprocess

scale = "scale=4;"

if len(sys.argv[:]) == 1:
    x = input("calc:")
    sysip = 'echo "{}{}" | bc'.format(scale, x)
    #sysip = 'echo "{}" | bc'.format(x)
    os.system(sysip)
elif len(sys.argv[:]) > 1:
    x = sys.argv[1:]
    for i in x:
        #sysip = 'echo "{}" | bc'.format(i)
        sysip = 'echo "{}{}" | bc'.format(scale, i)
        print("{}  = ".format(i))
        subprocess.run(sysip, shell=True)
