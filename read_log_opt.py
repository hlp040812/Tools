#!/usr/bin/env python
# coding: utf-8

import os, re

def read_log_opt(flog, dump=False):
#     flog = os.path.join(
#         os.path.expandvars('$ACNNHOME'), 
#         'tests/nn_fitting/OUT-pt9-reference-opt/opt.log')
    dlog = os.path.dirname(flog)
    nmlog = os.path.basename(flog)
    fout = os.path.join(dlog, nmlog+'.data')

    regexp = r'\s+\d+\s+\d+\%\s+-?\d+.?\d+\s+-?\d+.?\d+\s+-?\d+.?\d+\s+\d+\s+\d+.?\d+.'

    with open(flog, 'r') as fread:
        lines = fread.readlines()
        
    lout = []
    for line in lines:
        if re.match(regexp, line):
            lout.append(line)
    
    if dump in (True, False):
        if dump:
            with open(fout, 'w') as fwrite:
                fwrite.writelines(lout)
    else:
        raise Exception('dump must be "True" or "False", not {}'.format(type(dump)))
    
    return lout
