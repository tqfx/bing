#!/usr/bin/env python
# -*- coding : utf-8 -*-
import os
import re
import sys
import time
import json
import requests
from bs4 import BeautifulSoup

def get(i, datename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }  # set up user-agent

    url = "https://bing.ioliu.cn/"
    params = {"p": str(i)}  # set up parameters

    r = requests.get(
        url, params=params, headers=headers, timeout=10, allow_redirects=False
    )  # requests url

    print("log:", r.url, r.status_code)  # show status

    if 200 == r.status_code:  # requests successful
        items = []
        if os.path.exists(dataname):
            with open(datename, "r", encoding="utf-8") as f:
                items = json.load(f)

        soup = BeautifulSoup(r.text, "html.parser")
        divs = soup.find_all("div", class_="item")  # searuch the items
        for div in divs:
            info = div.h3.text

            date = div.em.text
            date = date.replace("-", "")

            # finding duplicate
            mark = False
            for item in items:
                if date in item["date"]:
                    mark = True
                    break
            if mark:
                continue

            url = div.a["href"]
            url = re.findall("photo/([^?]*)", url)[0]
            url = "https://cn.bing.com/th?id=OHR." + url + "_UHD.jpg"

            items.append({"date": date, "info": info, "url": url})

        items.sort(key=lambda x: x["date"], reverse=True)
        with open(datename, "w", encoding="utf-8") as f:
            json.dump(items, f)

        return True

    else:
        return False

def delay(i):
    for j in range(i):
        print(str(i - j), end="\r")
        time.sleep(1)

if __name__ == "__main__":
    argc = len(sys.argv)

    n = 0
    if 1 < argc:
        n = eval(sys.argv[1])
    dataname = "bing.json"
    if 2 < argc:
        dataname = sys.argv[2]

    i = 1
    while True:
        state = get(i, dataname)
        if i > n - 1:
            break
        if state:
            i += 1
            delay(5)
        else:
            delay(600)
