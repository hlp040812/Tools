#!/usr/bin/env python
# coding: utf-8

readme = '''

 # Check movie info:
 shkmovie.py -i cp2k-pos-1.pdb.0 cp2k-pos-1-shk.arc.1 cp2k-pos-1-shk.xyz.2
 
 # Shrink movie and write into cp2k-pos-1-shk.pdb:
 shkmovie.py -f cp2k-pos-1.pdb -r 10
 
 # Define your own shrink file name:
 shkmovie.py -f cp2k-pos-1.pdb -r 10 -o cp2k-pos-1-shk.pdb
 
 # avoid overwritting:
 # default is cover the existing outfile
 shkmovie.py -f cp2k-pos-1.pdb -r 10 -o cp2k-pos-1-shk.pdb -a
 
 # Transfer PDB to ARC (for MaterialStudio)
 pdb2arc.sh cp2k-pos-1-shk.pdb > cp2k-pos-1-shk.arc
 
 # Transfer PDB to XYZ (for ReacNetGenerator)
 pdb2xyz.sh cp2k-pos-1-shk.pdb > cp2k-pos-1-shk.xyz
 
 shkmovie.py --pdb2arcxyz 
     "pdb2arc.sh cp2k-pos-1-shk.pdb > cp2k-pos-1-shk.arc" 
     "pdb2xyz.sh cp2k-pos-1.pdb > cp2k-pos-1.xyz"
'''

import sys
from optparse import OptionParser


parser = OptionParser(usage=readme)

parser.add_option(
    "-f", "--infile", 
    type="string", 
    dest="infile",
    help="input file, support PDB XYZ"
)

parser.add_option(
    "-r", "--rate", 
    type="int", 
    dest="rate", 
    help="shrink rate"
)

parser.add_option(
    "-o", "--outfile", 
    type="string", 
    dest="outfile", 
    help='default="***-shk.***"'
)

parser.add_option(
    "-a", "--avoidoverwrite", 
    action="store_true", 
    dest="avoidoverwrite", 
    help="avoid outfile overwrite. default=None"
)

parser.add_option(
    "-i", "--info", 
    action="store_true",
    dest="info", 
    help="show information of movie files, support PDB XYZ ARC"
)

parser.add_option(
    "--pdb2arcxyz", 
    action="store_true",
    dest="pdb2arcxyz", 
    help="use the pdb2arc.sh and pdb2xyz.sh script"
)

(options, args) = parser.parse_args()

para = sys.argv
# print(para)
# print(options)
# print(args)
if len(para) == 1:
    parser.print_help()
    quit()

#################################################################
#################################################################

import linecache, os
from avoid_overwritting import new_file_name


def shkxyz(fname, shkname, shkratio):
    natoms = linecache.getline(fname, 1).strip()
    natoms = int(natoms)
    lframe = natoms + 2
    
    # count number of lines
    nlines = -1
    for nlines, _ in enumerate(open(fname, 'r')):
        nlines += 1
        
    if nlines % lframe != 0:
        raise Exception("Broken XYZ file.")
    nframes = nlines // lframe
    
    print("number of atoms = {}".format(natoms))
    print("number of frames = {} -> {}".
          format(nframes, nframes//shkratio))
    
    with open(shkname, 'w') as shk:
        for i in range(nframes//shkratio):
            for j in range(1, lframe+1):
                shk.write(
                    linecache.getline(fname, i*shkratio*lframe+j))


def shkpdb(fname, shkname, shkratio):
    title = linecache.getline(fname, 1)
    author = linecache.getline(fname, 2)

    # count number of lines
    nlines = -1
    for nlines, _ in enumerate(open(fname, 'r')):
        nlines += 1

    flag = 1
    count = 0
    with open(fname, "r") as f:
        while flag:
            if f.readline().strip().startswith("END"):
                flag = 0
            count += 1

    natoms = count - 5
    lframe = count - 2
    if (nlines - 2) % lframe != 0:
        raise Exception("Broken PDB file.")
    nframes = (nlines - 2) // lframe
    
    print("number of atoms = {}".format(natoms))
    print("number of frames = {} -> {}".
          format(nframes, nframes//shkratio))
    
    with open(shkname, 'w') as shk:
        shk.write(title)
        shk.write(author)
        for i in range(nframes//shkratio):
            # print("i = {}".format(i))
            for j in range(1, lframe+1):
                # print("j = {}".format(i*shkratio*lframe+j+2))
                shk.write(
                    linecache.getline(fname, i*shkratio*lframe+j+2))


def size_format(size):
    if size < 1024:
        return '%i' % size + 'size'
    elif 1024 <= size < 1024*1024:
        return '%.1f' % float(size/1024) + 'K'
    elif 1024*1024 <= size < 1024*1024*1024:
        return '%.1f' % float(size/1024/1024) + 'M'
    elif 1024*1024*1024 <= size < 1024*1024*1024*1024:
        return '%.1f' % float(size/1024/1024/1024) + 'G'
    
    
def info(fname):
    
    name, ext = os.path.splitext(fname)
    
    if ext.lower() == ".pdb" or \
    (name.lower().endswith(".pdb") and 
     ext.lower().lstrip('.').isdigit()):
        # count number of lines
        nlines = -1
        for nlines, _ in enumerate(open(fname, 'r')):
            nlines += 1
        
        flag = 1
        count = 0
        with open(fname, "r") as f:
            while flag:
                if f.readline().strip().startswith("END"):
                    flag = 0
                count += 1

        natoms = count - 5
        lframe = count - 2
        if (nlines - 2) % lframe != 0:
            raise Exception("Broken PDB file.")
        nframes = (nlines - 2) // lframe
        
        fsize = size_format(os.path.getsize(fname))
        
        print(" {} = {}".format(fname, fsize))
        print(" number of atoms = {}".format(natoms))
        print(" number of frames = {}".format(nframes))
        print(" number of lines = {}".format(nlines))
        
    elif ext.lower() == ".xyz" or \
    (name.lower().endswith(".xyz") and 
     ext.lower().lstrip('.').isdigit()):
        natoms = linecache.getline(fname, 1).strip()
        natoms = int(natoms)
        lframe = natoms + 2

        # count number of lines
        nlines = -1
        for nlines, _ in enumerate(open(fname, 'r')):
            nlines += 1

        if nlines % lframe != 0:
            raise Exception("Broken XYZ file.")
        nframes = nlines // lframe
        
        fsize = size_format(os.path.getsize(fname))
        
        print(" {} = {}".format(fname, fsize))
        print(" number of atoms = {}".format(natoms))
        print(" number of frames = {}".format(nframes))
        print(" number of lines = {}".format(nlines))
        
    elif ext.lower() == ".arc" or \
    (name.lower().endswith(".arc") and 
     ext.lower().lstrip('.').isdigit()):
        # count number of lines
        nlines = -1
        for nlines, _ in enumerate(open(fname, 'r')):
            nlines += 1

        flag = 1
        count = 0
        with open(fname, "r") as f:
            while flag:
                if f.readline().strip().startswith("end"):
                    flag = 0
                count += 1

        natoms = count - 6
        lframe = count - 1
        if (nlines - 2) % lframe != 0:
            raise Exception("Broken ARC file.")
        nframes = (nlines - 2) // lframe
        
        fsize = size_format(os.path.getsize(fname))

        print(" {} = {}".format(fname, fsize))
        print(" number of atoms = {}".format(natoms))
        print(" number of frames = {}".format(nframes))
        print(" number of lines = {}".format(nlines))

    else:
        raise Exception("Only support PDB, XYZ and ARC movie.")
    
    
#################################################################
#################################################################

if options.infile == options.info == options.pdb2arcxyz == None:
    parser.error("Need input file!")


if options.info:
    fnames = args
    for i, fname in enumerate(fnames):
        if i == 0:
            print("-----"*6)
        info(fname)
        print("-----"*6)


if options.infile:
    if options.rate == None:
        parser.error("Need shrink rate!")
    else:  # type(options.rate) == int
        fname = options.infile
        shkratio = options.rate
        name, ext = os.path.splitext(fname)

        if options.outfile == None:
            if options.avoidoverwrite == None:
                shkname = name + "-shk" + ext
            else:
                shkname = new_file_name(shkname = name + "-shk" + ext)
        else:
            if options.avoidoverwrite == None:
                shkname = options.outfile
            else:
                shkname = new_file_name(options.outfile)

        if ext.lower() == ".pdb":
            shkpdb(fname, shkname, shkratio)
        elif ext.lower() == ".xyz":
            shkxyz(fname, shkname, shkratio)
        else:
            parser.error("Only shrink PDB and XYZ movie.")

        print("Shrink \033[0;36m {} \033[0m ->  \033[0;36m {} \033[0m".
              format(fname, shkname))


if options.pdb2arcxyz:
    # in options, only pdb2arcxyz is True, others are all None
    len_options = len(options.__dict__)
    len_None = list(options.__dict__.values()).count(None)
    if len_None != len_options - 1:
        parser.error("using pdb2arc with other option is not allowed")

    for com in args:
        print("\033[0;36m Running... \033[0m", com)
        _ = os.system(com)
