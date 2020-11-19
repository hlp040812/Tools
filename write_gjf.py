#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.expanduser('~/Tools/')))
from avoid_overwritting import new_file_name


def check_gjf(path):
    '''check ".gjf" file in directory'''
    
    Files = os.listdir(path)
    checklist = []
    for file in Files:
        checklist.append(os.path.splitext(file)[-1])

    Str = '.gjf'
    if Str in checklist:
        return True
    else:
        return False


def write_gjf(output_path, format_file, 
              num_before_coord, num_after_coord, 
              num_atoms, num_frames, xyz, M=1):
    
    ## check output path
    if os.path.exists(output_path):
        if check_gjf(output_path):
            raise Exception('There is .gjf file in directory: "{}"'.format(output_path))
    else:
        print('Warning: No such file or directory: "{}"'
              .format(output_path))
    
    lines_input_1 = ''
    with open(format_file, 'r') as fread:
        for line in fread.readlines()[1:num_before_coord]:  # in this case, let's copy line 2-8
            lines_input_1 += line

    lines_input_2 = ''
    with open(format_file, 'r') as fread:
        for line in fread.readlines()[num_after_coord-1:]:  # in this case, let's copy line 18->end
            lines_input_2 += line

    for i, cords in  enumerate(xyz):
        output_file = os.path.join(output_path, '{}{}-M{}-{}.gjf'.format(xyz[0][0][0], num_atoms, M, i+1))
        with open(output_file, 'w') as fwrite:
            fwrite.write('%chk={}{}-M{}-{}.chk\n'.format(xyz[0][0][0], num_atoms, M, i+1))
            fwrite.write(lines_input_1)
            for cord in cords:
                fwrite.write('{:<5s}{:15.8f}{:15.8f}{:15.8f}\n'.format(cord[0], cord[1], cord[2], cord[3]))
            fwrite.write(lines_input_2)

