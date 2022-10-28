
# run cp2k on DELL
cp2k.ssmp cp2k.inp 2>&1 > cp2k.out &

##### Backup my Ubuntu into one .tar file
##### It's OK if got "tar: Exiting with failure status due to previous errors"
sudo su
tar -cvpzf /media/luping/UbuntuBackup/ubuntu_backup/system_backup@`date +%Y-%m+%d`.tar.gz --exclude=/proc --exclude=/tmp --exclude=/lost+found --exclude=/media --exclude=/mnt --exclude=/run --exclude=/sys -P /
tar -cvpzf /media/luping/UbuntuBackup/ubuntu_backup/work_backup@`date +%Y-%m+%d`.tar.gz --exclude=/media/luping/work/UbuntuSetup -P /media/luping/work/ 

##### Shut down Ubuntu after 180 minites or at 5PM.
sudo shutdown +180
sudo shutdown -h 16:20
sudo shutdown -h now

##### Ubuntu Document Viewer
evince
##### Ubuntu image viewer
eog
##### Ubuntu Chrome
google-chrome www.zhibo8.cc
##### Ubuntu open folder (GUI)
xdg-open .
nautilus .

reacnetgenerator -i cp2k-pos-1.xyz -t xyz -a C H O Cu Al Si -c 13.781 13.781 14.933 90.00 90.00 119.99

##### awk
# add "g09 " to each gjf file
ls *.gjf | awk '{print "g09 " $1}' > run.sh
##### sed
# print lines 1-250,
# add cp and ./M2-p1/ to 1-250 gjf file names,
# write into list.sh file.
ls M2-tot/Ta11-M2-*gjf | sed -n '1,250p' | sed -e 's/^/cp &/' -e 's/.*/& \.\/M2-p1\//' > list.sh
# remove line 6501 to end of file.
sed -i '6501,$d' ta11-M4.xyz
# remove first line
sed -i '1d' ta17-M2-123.xyz

# 140 205
pestat
qstat
showq

# take standard out and put it to a file. 
# It then take standard error and put it to the same location as standard out.
# Both streams are sent to a file.
acnnmain ta12-m5.json > log 2>&1 &

# take ownership of the mounted filesystem.
sudo chown -R luping:luping /media/luping/

# keep Sinopec desktop online by <ping jd.com> every 3 hours
crontab -e
* */3 * * * ping -c 2 jd.com 2>&1 > /dev/null &

# Linux associate file name extension with opening program
# Use Sublime default to open cp2k *.inp input files
# Firstly let Linux recognizes *.inp file
create a file:  ~/.local/share/mime/packages/application-x-inp.xml
Modify:  ~/.config/mimeapps.list

# automatic mount disk
/etc/fstab

jupyter nbconvert --to python xxx.ipynb

##### ssh without password:
##### from host A, user a -> to host B, user b
a@A:~> ssh-keygen -t rsa
a@A:~> ssh b@B mkdir -p .ssh
b@B's password: 
a@A:~> cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
b@B's password: 
a@A:~> ssh b@B

##### Find 'filename' in the whole drive.
sudo find / -depth -name filename
find `pwd` -name filename

##### Run <command> every 1 second
watch -n 1 -d "nvidia-smi"

##### This is a safe bin directory.
/usr/local/bin/

##### Give a full path with filename.
readlink -f filename

##### Output whereis python line by line.
whereis python | tr ' ' '\n'

##### open Mendeley Desktop
mendeleydesktop
some pdf downloaded from Mendeley are saved here:
/home/luping/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded

##### connect to wifi
sudo nmcli dev

##### Some conda commands
conda info
conda info --envs
conda info -e
conda activate python2
conda deactivate
conda activate py36
pip list

##### Just list files in zip file, but not unzip it.
unzip -l filename
##### unzip file into currunt directory.
unzip filename
##### zip dir1 and dir2 to myzipfile.zip
zip -r myzipfile.zip dir1 dir2

##### cluster
ssh -X luping@login1.stampede.tacc.utexas.edu
sshstampede
sshserver='ssh -X hanluping@159.226.204.97'

##### make files belong to the alexggp
chgrp -R alexggp /nfs/matsci-fserv/share/hanlu/Data4Alex/

##### This is the script to back up the cluster to /scratch/hanlu/Cluster-Backup
rsync -ahP submit-em64t-02.hpc.engr.oregonstate.edu:/nfs/matsci-fserv/share/hanlu/  /scratch/hanlu/Cluster-Backup
rsync -ahP luping@ranger.tacc.xsede.org:/work/02131/luping/  /scratch/hanlu/Work/

##### Remove ^M from PC files by vim
:%s/[ctrlkey+v and ctrl-key+M]//g
##### left right split
vim -O file1 file2
##### up down split
vim -o file1 file2
##### 2 tab pages
vim -p file1 file2

##### Block insert by vim
<Ctrl>+v 
select rows that you want to edit
<Shift>+i
insert something you need
<Esc>

##### Remove all files in the directry EXCEPT filename. (carefully!)
ls * | grep -v filename | xargs rm -rf
##### Remove all files in the directry EXCEPT "u" and "p" (carefully!)
shopt -s extglob
rm !(n|p)

##### directories recurse (all sub-directory will be search)
grep -iR keyword ~/cp2k-8.2/tests/

##### output appended with the file grows
tail -f cp2k.out

##### Display real IP address
wget -q -O - checkip.dyndns.org|sed -e 's/.*Current IP Address: //' -e 's/<.*$//'

##### Delete first line of every 1001 lines by vi
:let i=1 | while i <= line('$') | exe i . "delete" | let i += 1000 | endwhile
##### Delete first line of every 20 lines by MATLAB

##### rsync - Exclude files that are over a certain size
rsync -aPh --max-size=3.5G hanlu@submit-em64t-02.hpc.engr.oregonstate.edu:/ /Research/

##### copy single file to multiple folders
tee ~/folder1/test.txt ~/folder2/test.txt < ~/test.txt >/dev/null

140
source /opt/intel/oneapi/setvars.sh
source /opt/rh/devtoolset-10/enable
source /opt/intel/oneapi/mkl/latest/env/vars.sh
export PATH=/opt/OpenMPI/bin/:$PATH
export LD_LIBRARY_PATH=/opt/OpenMPI/lib/:$LD_LIBRARY_PATH
source /home/hanlp/opt/cp2k-9.1/tools/toolchain/install/setup
export PATH=$PATH:/home/hanlp/opt/cp2k-9.1/exe/local/
export LD_LIBRARY_PATH=/home/hanlp/bin:$LD_LIBRARY_PATH

205
source /opt/intel/oneapi/setvars.sh
source /opt/rh/devtoolset-10/enable
source /opt/intel/oneapi/mkl/latest/env/vars.sh
export PATH=/opt/openmpi/bin/:$PATH
export LD_LIBRARY_PATH=/opt/openmpi/lib/:$LD_LIBRARY_PATH
source /home/hanlp/opt/cp2k-9.1/tools/toolchain/install/setup
export PATH=$PATH:/home/hanlp/opt/cp2k-9.1/exe/local/

