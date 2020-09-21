#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.expanduser('~/Tools/')))
from read_xyz import Read_xyz
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
              num_atoms, num_frames, coord, el='Pt', M=1):
    
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
            
    for i in range(1, num_frames+1):
        output_file = os.path.join(output_path, '{}{}-M{}-{}.gjf'.format(el, num_atoms, M, i))
        with open(output_file, 'w') as fwrite:
            fwrite.write('%chk={}{}-M{}-{}.chk\n'.format(el, num_atoms, M, i))
            fwrite.write(lines_input_1)
        coord.loc[i, :].to_csv(output_file, mode='a+', 
                              index=False, header=False, 
                              sep=' ', quotechar=' ', float_format='%15.8f')
        with open(output_file, 'a+') as fwrite:
            fwrite.write(lines_input_2)
