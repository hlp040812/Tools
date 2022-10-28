#!/usr/bin/env python3
# coding: utf-8

import os, sys


if len(sys.argv) != 3:
    print("Example:\n rsync.py /home/luping/Downloads/libvdwxc-0.4.0.tar.gz /home/hanlp/")
    sys.exit()
    
# from desktop-dell to 205
path_local = sys.argv[1]
path_server = sys.argv[2]

if os.path.abspath(path_server).startswith("/home/luping") == True:
    path_server = path_server.replace("/home/luping", "/home/hanlp", 1) # replace just one time

#print(os.path.abspath(path_server))

com = 'rsync -aPh ' + path_local + ' hanlp@10.145.5.205:' + path_server

os.system(com)
print("\n {} \n Done \n".format(com))
