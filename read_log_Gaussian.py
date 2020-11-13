#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import sys, os, re, glob
from io import StringIO

def check_converge_criterion(mystr):
    '''
    If there is "Convergence criterion not met" keyword before the energy line like:
    
    >>>>>>>>>> Convergence criterion not met.
    SCF Done:  E(RTPSSh) =  -835.173022374     A.U. after   65 cycles
    
    then this energy will not come with a "Standard orientation".
    So just remove it.
    
    HOWEVER !!
    If keyword "IOp(5/13=1)" is given,
    though Convergence criterion not met, still dump a "Standard orientation".
    '''
    return 'Convergence criterion not met' not in mystr


def get_num(my_str):
    return float(my_str.split()[4])


def enprint(en):
    plt.plot(range(en.shape[0]), en, ".")
    plt.show()
    

class Read_log_Gaussian(object):
    '''
    Example:
    
    log = "../Gaussian/Ta9/10-steps-DFT-outputs/M2/Ta9-M2-96.log"
    t = read_log_Gaussian(log, element='Ta', num_atoms=9, steps=10)
    en = t.read_energy()
    xyz = t.read_xyz()
    
    or try:
    nn_fitting/gen_pgopt_input_from_Gaussian_logs.ipynb
    
    self.type = 
            "Full"
            "Convergence Problem"
            "Partial Done"
            "Energy and xyz NOT match"
    '''
    
    def __init__(self, log, element='Pt', num_atoms=9, steps=10, IOp=False):
        if IOp not in (True, False):
            raise TypeError("IOp must be True/False.")
        self.log = log
        self.num_atoms = num_atoms
        self.element = element
        self.steps = steps
        self.IOp = IOp
        self.badtypelist = ["Convergence Problem",
                         "Energy and xyz NOT match"]
        self.goodtypelist = ["Full",
                             "Partial Done"]
        self.type = None
        
        self.pre_check()
        self.en = self.read_energy()
        self.xyz = self.read_xyz()
        self.post_check()
        
    
    def pre_check(self):
        '''
        Check en.
        Generally, there are 10 or 20 energy frames in "Done", and
        there are 11 xyz frames of "Standard orientation".
        '''
        log = self.log
        popen_input_energy = 'grep "Done" {} | wc -l'.format(log)
        ndone = int(os.popen(popen_input_energy).read())
        # print(ndone)
        popen_input_so = 'grep "Standard orientation:" {} | wc -l'.format(log)
        nso = int(os.popen(popen_input_so).read())
        # print(nso)
        if ndone >= self.steps and nso == self.steps+1:
            self.type = "Full"
        elif ndone == 1 and nso == 1:
            self.type = "Convergence Problem"
        elif ndone > 1 and nso > 1:
            self.type = "Partial Done"
        
    
    def post_check(self):
        '''
        Check number of frames,
        energy == xyz 
        '''
        if self.type in self.goodtypelist:
            if self.en.shape[0] != self.xyz.shape[0]:
                self.type = "Energy and xyz NOT match"
            
            
    def frame_duplicate_check(self, index, counts):
        '''
        Check xyz.
        index and counts are return results of numpy.unique.
        '''
        # print(index)
        # print(counts)
        once = np.count_nonzero ( counts == 1 )
        twice = np.count_nonzero ( counts == 2 )
        
        if twice == 1 and np.count_nonzero(counts >= 3) == 0:
            index_duplicate = np.nonzero( counts == 2 )[0][0]
            index_last_frame = np.argmax(index)
            if not index_duplicate == index_last_frame:
                print('{}: duplicate frame is not the last frame!'.format(self.log))
        else:
            self.type = "Energy and xyz NOT match"
        
        
    def read_energy(self):
        log = self.log
        
        if self.IOp:
            popen_input_energy = 'grep "Done" ' + log + " | awk '{print $5}' "
            en_str = os.popen(popen_input_energy).read()
            energies = np.fromstring(en_str, dtype=np.float64, sep='\n')
            return energies
            
        else:
            popen_input_energy = 'grep -B 1 "Done" ' + log
            
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

            energies = full_energy[check_result].drop(['first_line'], axis=1).applymap(get_num)
            energies.index = range(1, energies.shape[0]+1)
            
            return energies.values.flatten() # return 1-D numpy array

        
    def read_xyz(self, num_tail=5):
        log = self.log
        nat = self.num_atoms
        popen_input_so = 'grep -A {} "Standard orientation:" '.format(nat+num_tail) + log
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
        
        if self.type in self.goodtypelist:
            xyz = np.fromstring(cords_str, dtype=np.float64, sep=' ')
            xyz = xyz.reshape(-1, nat, 3)
            (_, index, counts) = np.unique(xyz, axis=0, return_index=True, return_counts=True)
            self.frame_duplicate_check(index, counts)
            if self.type == "Energy and xyz NOT match":
                return False
            xyz = xyz [ np.sort(index) ]
            return xyz
            
        elif self.type in self.badtypelist:
            return False



if __name__ == "__main__":
    log = "/media/luping/Work/Practice/PGOPT-PROGRAMS/ACNN/tests/Gaussian/Ta9/10-steps-DFT-outputs/M2/Ta9-M2-96.log"
    t = Read_log_Gaussian(log, element='Ta', num_atoms=9, steps=10)
    en = t.read_energy()
    xyz = t.read_xyz()
    print(t.type)
    # print(en)
    # enprint(en)

