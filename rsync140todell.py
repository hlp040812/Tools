#!/usr/bin/env python3
# coding: utf-8

import os, sys


if len(sys.argv) != 3:
    print("Example:\n rsync.py /home/hanlp/libvdwxc-0.4.0.tar.gz  /home/luping/Downloads/")
    sys.exit()
    
# from desktop-dell to 205
path_server = sys.argv[1]
path_local = sys.argv[2]

if os.path.abspath(path_server).startswith("/home/luping") == True:
    path_server = path_server.replace("/home/luping", "/home/hanlp", 1) # replace just one time

#print(os.path.abspath(path_server))

com = 'rsync -aPh hanlp@10.145.5.140:' + path_server + ' ' + path_local

os.system(com)
print("\n {} \n Done \n".format(com))
