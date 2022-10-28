#!/usr/bin/env python
# coding: utf-8

import os


## files below will be removed!!
toremove = ["COLVAR", "HILLS", "PLUMED.OUT", "TIMING",
            "gausshills.dat", "fes.dat", "uwall"]


## files with such extensions to be removed!!
extensions = [".wfn", ".out", ".ener", ".restart"]


def is_remove(filename):
    name, extension = os.path.splitext(filename)
    if extension in extensions:
        flag = 1
    elif extension.startswith(".bak-") and name.endswith("-RESTART.wfn"):
        flag = 1
    elif extension.startswith(".bak-") and name.endswith(".restart"):
        flag = 1
    elif extension in [".pdb", ".xyz"] and name.endswith("-pos-1"):
        flag = 1
    elif extension.split(".")[-1].isdigit() and name in ["gausshills.dat", "fes.dat"]:
        flag = 1
    else:
        flag = 0
    return flag


remove_list = []

for file in os.listdir("./"):
    if os.path.isfile(file):
        if is_remove(file):
            remove_list.append(file)
        elif file in toremove:
            remove_list.append(file)

# Done generate remove_list


# if "TIMING" in os.listdir("./"):
#     remove_list.append("TIMING")
# elif "COLVAR" in os.listdir("./"):
#     remove_list.append("COLVAR")
# elif "HILLS" in os.listdir("./"):
#     remove_list.append("HILLS")
# elif "PLUMED.OUT" in os.listdir("./"):
#     remove_list.append("PLUMED.OUT")
# elif "gausshills.dat" in os.listdir("./"):
#     remove_list.append("gausshills.dat")
# elif "fes.dat" in os.listdir("./"):
#     remove_list.append("fes.dat")


columnlist = "\n ".join(remove_list)
mymessage1 = "\033[0;31m {}\033[0m \n will be removed.\n[y/n]\n[no] >>> ".format(columnlist)
yesno = input(mymessage1)
if yesno in ["yes", "y"]:
    for f in remove_list:
        os.remove(f)
        # pass
    mymessage2 = "\033[0;36m {} \033[0m removed.\n".format(remove_list)
    print(mymessage2)

