#!/usr/bin/env python
# -*- coding : utf-8 -*-
import os
import sys
import json

data = "bing.json"
prefix = "image"

if 1 < len(sys.argv):
    data = sys.argv[1]
if 2 < len(sys.argv):
    prefix = sys.argv[2]

with open(data, "r", encoding="utf-8") as f:
    items = json.load(f)
items.sort(key=lambda x: x["date"], reverse=True)
with open(data, "w", encoding="utf-8") as f:
    json.dump(items, f)

with open(os.path.splitext(data)[0] + ".sh", "wb") as f:
    cmd = "#!/usr/bin/env bash\nmkdir " + prefix + "\n"
    f.write(cmd.encode("utf-8"))
    for item in items:
        url = ' -c "' + item["url"] + '"'
        out = ' -O "' + prefix + "/" + item["date"] + '.jpg"'
        cmd = "wget" + url + out + "\n"
        f.write(cmd.encode("utf-8"))
