#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import sys, os
from io import StringIO
import re

pd.options.display.max_rows = None
pd.options.display.max_colwidth = 100


def check_converge_criterion(my_str):
    return 'Convergence criterion not met' not in my_str


def get_num(my_str):
    return my_str.split()[4]


def read_log_Gaussian(log_file, element='Pt', num_atoms=9, num_tail=5):
    ######## First, read energy ##########
    # Reading energy is more complicated than I thought.
    # Some energy do NOT meet Convergence criterion, have to get rid of them.
    
    # These are two ways to make energies as <float>.
    # 1, np.array
    # 2, use pandas.DataFrame in this case
    # popen_input_energy = 'grep "SCF Done:  E(RTPSSh) =" ' + log_file + ' | awk \'{print $5}\''
    # # energies = np.fromstring(os.popen(popen_input_energy).read(), dtype=float, sep='\n')
    # energies = pd.read_csv(StringIO(
    #            os.popen(popen_input_energy).read()), sep='\n', header=None, names=['energy'])
    
#     popen_input_energy = 'grep -B 1 "SCF Done:  E(RTPSSh) =" ' + log_file
    popen_input_energy = 'grep -B 1 "SCF Done:  E" ' + log_file
    screen_energy = pd.read_csv(StringIO(os.popen(popen_input_energy).read()), sep='\n', header=None)
    screen_energy = screen_energy[screen_energy.iloc[:, 0] != '--']
    screen_energy.index = range(screen_energy.shape[0])
    first_line = screen_energy.iloc[range(0,screen_energy.shape[0],2), 0]
    first_line.index = range(int(screen_energy.shape[0]/2))
    energy_line = screen_energy.iloc[range(1,screen_energy.shape[0],2), 0]
    energy_line.index = range(int(screen_energy.shape[0]/2))
    full_energy = pd.concat([first_line, energy_line], axis=1)
    full_energy.columns = ['first_line', 'energy_line']
    check_result = full_energy.iloc[:,0].map(check_converge_criterion)
#     try:
#         print('{}/{}: Convergence criterion not met = {}'.format\
#               (log_file.split('/')[-2], log_file.split('/')[-1], check_result.value_counts()[False]))
#     except KeyError:
#         pass
    energies = full_energy[check_result].drop(['first_line'], axis=1).applymap(get_num)
    energies.index = range(1, energies.shape[0]+1)
    ######## Done read energy ##########
    
   
    ######## Second, read Coordinates as float64. ##########
#     full_xyz = os.popen('grep -A {} "Standard orientation:" '.format(num_atoms+num_tail) + log_file).read()
    
#     if num_frames == 1:
#         skip_rows = np.array([0,1,2,3,4,12])
#     elif num_frames > 1:
#         skip_rows = np.empty(0, dtype=int)
#         for i in range(num_frames+1):
#             skip_rows = np.hstack(
#                                 (skip_rows,
#                                 np.arange(i*(num_atoms+num_tail+2), i*(num_atoms+num_tail+2)+num_tail)))
#             skip_rows = np.hstack(
#                                 (skip_rows,
#                                 np.arange(i*(num_atoms+num_tail+2)+num_atoms+num_tail, 
#                                           i*(num_atoms+num_tail+2)+num_atoms+num_tail+1)))
#             if i < num_frames:
#                 skip_rows = np.hstack((skip_rows, i*(num_atoms+num_tail+2)+num_atoms+num_tail+1))
        
#     xyz = pd.read_csv(StringIO(full_xyz),
#                     sep='\s+',
#                     header=None,
#                     names=['x','y','z'],
#                     usecols=[3,4,5],
#                     skiprows=skip_rows)
#     xyz.insert(loc=0, column=element, value=((element+' ')*xyz.shape[0]).split())
    
#     # Define DataFrame index
#     if xyz.shape[0] % num_atoms != 0:
#         print('Warning: \n{}/{}: Should be {} atoms in one frame.'.format\
#               (log_file.split('/')[-2], log_file.split('/')[-1], num_atoms))
#     num_loop = int(xyz.shape[0] / num_atoms)
#     index_layer_1 = np.array([], dtype=np.int64)
#     for i in range(num_loop):
#         index_layer_1 = np.hstack((index_layer_1, np.ones(num_atoms, dtype=np.int64) * (i+1)))
#     index_layer_2 = np.arange(1, num_atoms*(num_loop)+1)
#     my_index = [index_layer_1, index_layer_2]
#     xyz.index = my_index
    ######### Done. read Coordinates as float64. ##########
    
    
    ######## Second, read Coordinates as string. ##########
    popen_input_so = 'grep -A {} "Standard orientation:" '.format(num_atoms+num_tail) + log_file
    # os.popen(popen_input_so).read()
    # '[-]?[0-9]+\.[0-9]+'   ## float re
    # '\-?[0-9]+'            ## int re
    # '[-]?[0-9]+\.?[0-9]*'  ## float or int re
    ### This regular expression: float+float+float
    cords_str_list = re.findall(
        '[-]?[0-9]+\.?[0-9]+\s+[-]?[0-9]+\.?[0-9]+\s+[-]?[0-9]+\.?[0-9]+', 
        os.popen(popen_input_so).read())
    cords_str = ''
    for i in cords_str_list:
        cords_str = cords_str + i + '\n'
    
    xyz = pd.read_csv(StringIO(cords_str), sep='\n', header=None, names=['cordinates'])
    xyz.insert(loc=0, column=element, value=((element+' ')*xyz.shape[0]).split())
    
    # Define DataFrame index
    if xyz.shape[0] % num_atoms != 0:
        print('Warning: \n{}/{}: Should be {} atoms in one frame.'
              .format(log_file.split('/')[-2], log_file.split('/')[-1], num_atoms))
#     num_loop = int(xyz.shape[0] / num_atoms)
#     index_layer_1 = np.array([], dtype=np.int64)
#     for i in range(num_loop):
#         index_layer_1 = np.hstack((index_layer_1, np.ones(num_atoms, dtype=np.int64) * (i+1)))
#     index_layer_2 = np.arange(1, num_atoms*(num_loop)+1)
#     my_index = [index_layer_1, index_layer_2]
    my_index = pd.MultiIndex.from_product(
        [range(1, int(xyz.shape[0] / num_atoms)+1), range(1, num_atoms+1)], 
        names=['layer1', 'layer2'])
    xyz.index = my_index
    ######## Done. read Coordinates as string. ##########
    
    
    ######### Remove the duplicates of the frames. ##########
#     print(energies.index[energies.duplicated(keep=False)].tolist())
#     print(xyz.index[xyz.duplicated(keep=False)].tolist())
    energies.drop_duplicates(inplace=True)
    xyz.drop_duplicates(inplace=True)
#     print(energies.index.tolist())
#     num_frames_energy = energies.shape[0]
#     num_frames_xyz = int(xyz.shape[0] / num_atoms)
    if xyz.shape[0] % num_atoms != 0:
        print('Warning: \n{}/{}: Should be {} atoms in one frame after drop_duplicates.'
              .format(log_file.split('/')[-2], log_file.split('/')[-1], num_atoms))
    if xyz.index.remove_unused_levels().levels[0].tolist() != energies.index.tolist():
        print('{}/{}: xyz frame != energies frame. (Something went wrong)'
              .format(log_file.split('/')[-2], log_file.split('/')[-1]))
    ######### Done. Remove the duplicates of the frames. ##########
    
    return energies, xyz, num_atoms


############### Check "SCF Done" and "Standard orientation" manually. ##################
# for i in range(num_logs):
#     log_file = full_inputs.loc[i, 'log_file']
    
#     popen_input_energy = 'grep "SCF Done:  E(RTPSSh) =" ' + log_file + ' | awk \'{print $5}\''
#     energies = pd.read_csv(StringIO(os.popen(popen_input_energy).read()), sep='\n', header=None, names=['energy'])
    
#     popen_input_so = 'grep "Standard orientation:" ' + log_file
#     so = pd.read_csv(StringIO(os.popen(popen_input_so).read()), sep='\n', header=None, names=['so'])
    
#     if so.shape[0] <= energies.shape[0]:
#         print(log_file.split('/')[-2],log_file.split('/')[-1], ': xyz <= energy', so.shape[0]-energies.shape[0])
# #     elif so.shape[0] - energies.shape[0] == 1:
# #         print(log_file, ': standard orientation - SCF Done = 1. GOOD!')


if __name__ == "__main__":
    ## Convergence criterion==2
    log_test = os.path.join(
        os.path.expandvars('$ACNNHOME'), 
        'tests/Gaussian/Pt7-4850/output_files/Pt7-5/Pt7-287.log')
#     ## Normal
#     log_test = os.path.join(
#         os.path.expandvars('$ACNNHOME'), 
#         'tests/Gaussian/Pt7-4850/output_files/Pt7-2/Pt7-63.log')
#     ## xyz==energy==1
#     log_test = os.path.join(
#         os.path.expandvars('$ACNNHOME'), 
#         'tests/Gaussian/Pt7-4850/output_files/Pt7-2/Pt7-94.log')
#     ## xyz==energy
#     log_test = os.path.join(
#         os.path.expandvars('$ACNNHOME'), 
#         'tests/Gaussian/Pt7-4850/output_files/Pt7-10/Pt7-485.log')
    
    energies, xyz, num_atoms = read_log_Gaussian(log_test)

