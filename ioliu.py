#!/usr/bin/env python3
# -*- coding : utf-8 -*-
import os
import re
import time
import json
import sys

try:
    import requests
    import urllib3
except:
    os.system("python3 -m pip install -U requests")
    try:
        import requests
        import urllib3
    except:
        print("error:", "import requests")
        exit()

try:
    from bs4 import BeautifulSoup
except:
    os.system("python3 -m pip install -U bs4")
    try:
        from bs4 import BeautifulSoup
    except:
        print("error:", "import bs4")
        exit()


def get(url, i):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }  # set up user-agent

    params = {"p": str(i)}  # set up parameters

    r = requests.get(
        url, params=params, headers=headers, timeout=10, allow_redirects=False
    )  # requests url

    print("log:", r.url, r.status_code)  # show status

    if r.status_code == 200:  # requests successful
        dirlist = os.listdir(".")  # search the data file
        if data in dirlist:
            with open(data, "r", encoding="utf-8") as f:
                inlist = json.load(f)
        else:
            inlist = []

        soup = BeautifulSoup(r.text, "html.parser")
        itemlist = soup.find_all("div", class_="item")  # searuch the items
        for div in itemlist:
            info = div.h3.text

            date = div.em.text
            date = date.replace("-", "")

            # finding duplicate
            mark = False
            for img in inlist:
                if date in img["date"]:
                    mark = True
                    break
            if mark:
                continue

            src = div.a["href"]
            src = re.findall("photo/([^?]*)", src)[0]
            src = "https://cn.bing.com/th?id=OHR." + src + "_UHD.jpg"

            inlist.append({"info": info, "date": date, "src": src})

        inlist = sorted(inlist, key=lambda img: img["date"], reverse=True)
        with open(data, "w", encoding="utf-8") as f:
            json.dump(inlist, f)

        return True

    else:
        return False


def delay(i):
    for j in range(i):
        print(str(i - j), end="\r")
        time.sleep(1)


if __name__ == "__main__":
    url = "https://bing.ioliu.cn/"
    data = "bing.json"
    i = 1
    while i < 145:
        if get(url, i):
            i += 1
            delay(5)
        else:
            delay(600)
