#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_colwidth = 100


# ### Load data from structure file

# In[2]:


class Read_xyz(object):
    def __init__(self, import_file, num_header=2):
        '''
        ===== Use Read_xyz like: =====
        st = Read_xyz('./OUT-pt9-reference-opt/opt_structs.xyz.0')
        en, xyz = st.get_xyz()
        enarr, xyzarr = st.df2array()

        self.num_header -> header of each frame
        self.num_frames
        self.num_atoms
        self.num_lines
        '''
        
        self.import_file = import_file
        self.num_header = num_header
        
        ## Define # of lines and # of atoms
        self.num_lines = 0
        with open(import_file, 'r') as f:
            for line in f:
                if self.num_lines == 0:
                    if int(line):
                        self.num_atoms = int(line)
                if not line.split():
                    print('Warning: {} is a blank line, better check.'.format(self.num_lines+1))
                else:
                    self.num_lines += 1

        ## Define # of frames
        # if it is a integer number
        if np.ceil(self.num_lines / (self.num_atoms+self.num_header)) != \
        self.num_lines / (self.num_atoms+self.num_header):
            raise ValueError('number of frames should be a int.')
        self.num_frames = int(self.num_lines / (self.num_atoms+self.num_header))


    def get_xyz(self):
        '''
        coordinate  ->  "self.coord" dataframe and "self.cood_array" numpy array
        energy      ->  "self.en"    dataframe and "self.en_array"   numpy array
        '''
        
        ## Define # of skipped rows
        a = np.arange(0,  self.num_lines,  self.num_atoms+self.num_header)
        b = np.arange(1,  self.num_lines,  self.num_atoms+self.num_header)
        c = np.setdiff1d(np.setdiff1d(np.arange(self.num_lines), a), b) # c = total - a - b
        if not np.all(np.union1d(np.union1d(a,b), c) == np.arange(self.num_lines)):
            # check if a+b+c=total?
            print('Error: please check skip rows.')
        skip_rows_1 = np.union1d(a,b) if np.intersect1d(a,b).size == 0 else np.NaN
        skip_rows_2 = np.union1d(a,c) if np.intersect1d(a,c).size == 0 else np.NaN

        ## Define "coord" DataFrame index
        index_layer_1 = np.array([], dtype=np.int64)
        for i in range(self.num_frames):
            index_layer_1 = np.hstack((index_layer_1, np.ones(self.num_atoms, dtype=np.int64) * (i+1)))
        index_layer_2 = 1 + np.setdiff1d(np.arange(self.num_lines), skip_rows_1)
        coord_index = [index_layer_1, index_layer_2] \
        if index_layer_1.shape == index_layer_2.shape else np.NaN
        
        ## get "en"
        self.en = pd.read_csv(self.import_file, 
                                delimiter='=',  
                                header=None, 
                                skiprows=skip_rows_2)
        self.en.index = range(1, self.num_frames+1) if self.en.shape[0] == self.num_frames else np.NaN

        ## get "coord"
        self.coord = pd.read_csv(self.import_file, 
                                delimiter='\s+',  
                                header=None, 
                                skiprows=skip_rows_1)
        self.coord.index = coord_index
        
        ## Check the data frame
        if not         isinstance(self.num_atoms, int) and \
        isinstance(self.num_lines, int) and \
        isinstance(self.num_frames, int):
            print('Warning: num_atoms, num_lines, num_frames should be int.')
        if not \
        self.coord.ndim == 2 and \
        self.coord.shape[0] == self.num_lines - skip_rows_1.shape[0] == self.num_atoms * self.num_frames and \
        self.num_lines == skip_rows_1.shape[0] + self.coord.shape[0]:
            print('Warning: need check data frame, num_lines, skip_rows, num_atoms, num_frames.')
        else:
            print('Looks fine.')

        return self.en, self.coord
    
    def df2array(self):
        '''
        Keep in mind:
        run "get_xyz" before "df2array"
        Pandas DataFrame  "en"       and "coord"        index are from 1
        NumPy Array       "en_array" and "coord_array"  index are from 0
        '''
        self.en_array = self.en.values
        self.coord_array = self.coord.values.reshape(self.num_frames, self.num_atoms, self.coord.shape[1])
        
        return self.en_array, self.coord_array


# ### test

# In[3]:


if __name__ == "__main__":
    t = Read_xyz('./OUT-pt9-reference-opt/opt_structs.xyz.0')
    en, xyz = t.get_xyz()
    enarr, xyzarr = t.df2array()


# In[ ]:




