#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os
from read_xyz import Read_xyz
from avoid_overwritting import new_file_name


# In[ ]:


def write_xyz(fout, xyz, en, num_atoms, name_molecule=None):
    '''
    ===== Use write_xyz like: =====
    write_xyz(fout='OUT-pt13-test/no_plane_structs.xyz',
              xyz=no_plane_xyzarr,
              en=no_plane_enarr,
              num_atoms=st.num_atoms)
    
    xyz should be np.array like:
        [['Pt'    0.92479008     0.08094939     1.74390052]
        ['Pt'    -0.91225292     1.89410339     0.74539328]
        ['Pt'    -1.38613011    -0.94576637    -2.97381683]
        ['Pt'    -2.85864802     0.36223171    -0.12155428]]

    en should be np.array like:
        [['PRE:0'   -1073.85975565]
        ['PRE:1'    -1073.87047319]
        ['PRE:2'    -1073.88442272]
        ['PRE:3'    -1073.88708975]]
    '''

    fout = os.path.join(fout)
    fout = new_file_name(fout)

    with open(fout, 'w') as f:
        for cords, e in zip(xyz, en):
            f.write('{}\n'.format(num_atoms))
            if name_molecule:
                f.write('{} = {:15.8f}\n'.format(name_molecule, e))
            else:
                f.write('{} = {:15.8f}\n'.format(e[0], e[1]))
            for cord in cords:
                f.write('{:>7s}{:15.8f}{:15.8f}{:15.8f}\n'.format(cord[0], cord[1], cord[2], cord[3]))


# In[ ]:


if __name__ == "__main__":
    pass

