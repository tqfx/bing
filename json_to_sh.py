#!/usr/bin/env python3
import os
import json


def dealname(name):
    name = name.split("©")[0]
    if "(" in name[-1]:
        name = name[:-1:]
    if "（" in name[-1]:
        name = name[:-1:]
    while " " in name[-1]:
        name = name[:-1:]
    return name


data = "bing.json"

with open(data, "r", encoding="utf-8") as f:
    inlist = json.load(f)
inlist = sorted(inlist, key=lambda img: img["date"], reverse=True)
with open(data, "w", encoding="utf-8") as f:
    json.dump(inlist, f)

with open("bing.sh", "w", encoding="utf-8") as f:
    pwd = "img"
    f.write("#!/usr/bin/bash\nmkdir " + pwd + "\n")
    for img in inlist:
        f.write("mkdir " + pwd + "/" + img["date"] + "\n")
        url = ' -c "' + img["src"] + '"'
        out = ' -O "' + pwd + "/" + img["date"] + "/" + dealname(img["info"]) + '.jpg"'
        f.write("wget" + url + out + "\n")
