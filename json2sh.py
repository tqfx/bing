#!/usr/bin/env python
# -*- coding : utf-8 -*-
import os
import sys
import json

data = "bing.json"
prefix = "image"

if 1 < len(sys.argv):
    data = sys.argv[-1]

with open(data, "r", encoding="utf-8") as f:
    items = json.load(f)
items.sort(key=lambda x: x["date"], reverse=True)
with open(data, "w", encoding="utf-8") as f:
    json.dump(items, f)
with open(os.path.splitext(data)[0] + ".sh", "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env bash\nmkdir " + prefix + "\n")
    for item in items:
        url = ' -c "' + item["url"] + '"'
        out = ' -O "' + prefix + "/" + item["date"] + '.jpg"'
        f.write("wget" + url + out + "\n")
