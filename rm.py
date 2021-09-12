#!/usr/bin/env python3
import os
import time


def rmimg(pwd):
    if pwd[-1] != "/":
        pwd += "/"
    dirlist = os.listdir(pwd)
    sorted(dirlist)
    for name in dirlist:
        if os.path.isdir(pwd + name):
            rmimg(pwd + name)
        if os.path.isfile(pwd + name):
            size = os.path.getsize(pwd + name) / 1024 / 1024
            if size < 0.1:
                os.remove(pwd + name)
                print("rm {}".format(pwd + name))
                if len(dirlist) == 1:
                    os.rmdir(pwd)
                    print("rmdir {}".format(pwd))


rmimg("img")
t = os.path.getmtime(".")
t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
print(t)
