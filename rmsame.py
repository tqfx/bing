#!/usr/bin/env python
import os
import hashlib
import sys


flag_rename = 0
flag_remove = 1
flag_rename_size = 1
flag_remove_empty = 1


def run(pwd):
    removeset = set()

    filelist = []
    for dirpath, dirnames, filenames in os.walk(pwd):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            filename = filename.replace('\\', '/')
            size = os.path.getsize(filename)
            if size > 0:
                filelist.append(filename)
            elif flag_remove_empty:
                removeset.add(filename)

    filelen = len(filelist)
    for i in range(filelen):
        filename1 = filelist[i]
        size1 = os.path.getsize(filename1)
        m1 = str()
        for j in range(filelen):
            if i == j:
                continue
            filename2 = filelist[j]
            size2 = os.path.getsize(filename2)
            if size1 == size2:
                if str() == m1:
                    with open(filename1, "rb") as f1:
                        m1 = hashlib.md5(f1.read()).hexdigest()
                with open(filename2, "rb") as f2:
                    m2 = hashlib.md5(f2.read()).hexdigest()
                if m1 == m2:
                    t1 = os.path.getmtime(filename1)
                    t2 = os.path.getmtime(filename2)
                    if t1 > t2:
                        removeset.add(filename1)
                    else:
                        removeset.add(filename2)

    for filename in removeset:
        if flag_remove:
            os.remove(filename)
            print("remove", filename)

    renamelist = []

    filelist.clear()
    for dirpath, dirnames, filenames in os.walk(pwd):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            filename = filename.replace('\\', '/')
            filelist.append(filename)

    for filename in filelist:
        dirpath, basename = os.path.split(filename)
        namefix = os.path.splitext(basename)[-1]
        if flag_rename_size:
            namebase = "%08u" % (os.path.getsize(filename))
            sizename = os.path.join(dirpath, namebase + namefix)
            sizename = sizename.replace('\\', '/')
            idx = 0
            while sizename in renamelist:
                sizename = os.path.join(dirpath, namebase + '_%u' % (idx) + namefix)
                sizename = sizename.replace('\\', '/')
                idx += 1
        else:
            idx = 10000
            namebase = "%u" % (idx * os.path.getmtime(filename))
            sizename = os.path.join(dirpath, namebase + namefix)
            sizename = sizename.replace('\\', '/')
            while sizename in renamelist:
                idx *= 10
                namebase = "%u" % (idx * os.path.getmtime(filename))
                sizename = os.path.join(dirpath, namebase + namefix)
                sizename = sizename.replace('\\', '/')
        renamelist.append(sizename)

    filelen = len(filelist)
    renamelen = len(renamelist)
    if filelen != renamelen:
        print(filelen, renamelen)
        exit()

    for i in range(filelen):
        if filelist[i] != renamelist[i]:
            if flag_rename:
                os.rename(filelist[i], renamelist[i])
                print(renamelist[i], '<-', filelist[i])


for pwd in sys.argv[1:]:
    run(pwd)
