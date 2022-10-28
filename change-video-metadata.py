#!/usr/bin/env python
# coding: utf-8


from mutagen.mp4 import MP4
import os


os.chdir("/media/luping/9B96-6A33/にほんご/芥末-大家的日语/录播课")
os.getcwd()


def remove_tags(file_path):
    movie_tags = MP4(file_path)
    movie_tags.clear()
    movie_tags.save()


for root, dirs, files in os.walk("./"):
    if files:
        # print(root, dirs, files)
        for f in files:
            if f[0].isdigit():
                filename = os.path.join(root, f)
                remove_tags(filename)

