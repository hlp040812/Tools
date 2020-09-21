#!/usr/bin/env python
# coding: utf-8

import os

def new_file_name(x):
    '''
    For example:
    fout = new_file_name('./OUT-pt9-reference-opt/opt_300_structs.xyz')
    '''
    i = 0
    y = x + '.' + str(i)
    while os.path.isfile(y):
        i += 1
        y = x + '.' + str(i)
    print(y, '  is used.')
    return y

def new_path_name(x):
    i = 0
    y = x + '.' + str(i)
    while os.path.exists(y):
        i += 1
        y = x + '.' + str(i)
    return y
