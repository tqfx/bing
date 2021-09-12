#!/usr/bin/env python
# -*- coding : utf-8 -*-
import os
import re
import sys
import time
import json
import requests
from bs4 import BeautifulSoup


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

            url = div.a["href"]
            url = re.findall("photo/([^?]*)", url)[0]
            url = "https://cn.bing.com/th?id=OHR." + url + "_UHD.jpg"

            inlist.append({"info": info, "date": date, "url": url})

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
    n = 0
    if 1 < len(sys.argv):
        n = eval(sys.argv[-1])
    i = 1
    while i < n + 1:
        if get(url, i):
            i += 1
            delay(5)
        else:
            delay(600)
