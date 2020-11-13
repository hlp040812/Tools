#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
from read_log_Gaussian import Read_log_Gaussian


class Remove_abnormal_energy(object):
    '''
    If E(i+1) - E(i) > 0.005 hartree, remove the higher energy.
    Example is at the end of this file.
    '''
    def __init__(self, en, xyz):
        self.ien = en
        self.ixyz = xyz
        self.en_threshold = 0.005  # hartree
        self.fit_threshold = 0.3
        self.en, self.xyz = self.remove()
    
    
    def diff(self, en):
        # Return the index of difference of energies.
        # every energy step - previous step
        idxdiff = np.argwhere( en[1:]-en[:-1] > self.en_threshold )
        return idxdiff + 1
    
    
    def remove(self):
        en = self.ien
        xyz = self.ixyz
        idxdiff = self.diff(self.ien).flatten()
        while idxdiff.size != 0:
            en = np.delete(en, idxdiff, axis=0)
            xyz = np.delete(xyz, idxdiff, axis=0)
            idxdiff = self.diff(en).flatten()
        return en, xyz



if __name__ == "__main__":
    log = os.path.join(
            os.path.expandvars('$ACNNHOME'), 
            'tests/Gaussian/Ta13/10-steps-DFT-outputs/M2/Ta13-M2-533.log')
    t = Read_log_Gaussian(log, element='Ta', num_atoms=13, steps=20, IOp=True)
    r = Remove_abnormal_energy(t.en, t.xyz)
    print(r.en)
    print(r.xyz)


# In[ ]:





# ### Linear fitting backup
# 
# ```python
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn import preprocessing
# 
# def is_decreasing(en, iprint=False):
#     '''
#     en should be 1-D numpy array.
#     '''
#     nen = preprocessing.scale(en)  # Normalize
#     k, b = np.polyfit(range(en.shape[0]), nen, 1)
#     print('{:.3f} x + {:.3f}'.format(k, b))
#     if iprint:
#         p1d = np.poly1d([k, b])
#         plt.plot(range(nen.shape[0]), nen, ".")
#         plt.plot(range(nen.shape[0]), p1d(range(nen.shape[0])))
#         plt.show()
#     
#     return k < 0
# 
# data = np.array([-1073.84327841,
# -1073.86144826,
# -1073.87868635,
# -1073.88353983,
# -1073.89579241,
# -1073.85681163,
# -1073.90124396,
# -1073.90582007,
# -1073.90922261,
# -1073.90926417]
# )
# is_decreasing(data, iprint=True)
# ```

# ### curve fitting backup
# 
# ```python
# import sys, os, re, glob
# sys.path.append(os.path.dirname(os.path.expanduser('~/Tools/')))
# from read_log_Gaussian import Read_log_Gaussian
# import numpy as np
# from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt
# from sklearn import preprocessing
# import warnings
# from scipy.optimize import OptimizeWarning
# warnings.simplefilter("error", OptimizeWarning)
# 
# class Remove_abnormal_energy(object):
#     '''
#     If E(i+1) - E(i) > 0.005 hartree, remove the higher energy.
#     '''
#     def __init__(self, en, xyz):
#         self.ien = en
#         self.ixyz = xyz
#         self.en_threshold = 0.005  # hartree
#         self.fit_threshold = 0.3
#         self.en, self.xyz = self.remove()
#     
#     
#     def exp_func(self, x, a , b, c, d):
#         return a * np.exp(b * x + c) + d
# 
# 
#     def exp_fit(self, y, iprint=False):
#         x = np.arange(y.shape[0])
#         p3 = 0.2
#         p0 = [1, -1, p3, -1]
#         while p3 < 3:
#             try:
#                 print('try {}'.format(p0))
#                 param, _ = curve_fit(self.exp_func, x, y, p0=p0)
#             except (OptimizeWarning, RuntimeError):
#                 print('{} got OptimizeWarning or RuntimeError.'.format(p0))
#                 p3 += 0.2
#                 p0 = [1, -1, p3, -1]
#                 continue
#             else:
#                 print('{} I am in else.'.format(p0))
#                 break
# 
#         print(param)
#         if iprint:
#             plt.figure()
#             myplt = plt.plot(x, y, ".")
#             myplt = plt.plot(x, self.exp_func(x, *param), "r--")
#             plt.show()
#         return param
#     
#     
#     def enprint(self):
#         y = preprocessing.scale(self.ien)  # Normalize
#         x = np.arange(y.shape[0])
#         param = self.exp_fit(y, iprint=True)
#         yp = self.exp_func(x, *param)
#         print(y)
#         print(yp)
#         print(y-yp)
# 
# 
#     def diff(self, en):
#         # Return the index of difference of energies.
#         # every energy step - previous step
#         idxdiff = np.argwhere( en[1:]-en[:-1] > self.en_threshold )
#         return idxdiff
#     
#     
#     def remove(self):
#         en = self.ien
#         xyz = self.ixyz
#         idxdiff = self.diff(self.ien).flatten()
#         while idxdiff.size != 0:
#             en = np.delete(en, idxdiff+1, axis=0)
#             xyz = np.delete(xyz, idxdiff+1, axis=0)
#             idxdiff = self.diff(en).flatten()
#         return en, xyz
# 
# ```
