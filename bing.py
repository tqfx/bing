#!/usr/bin/env python
# -*- coding : utf-8 -*-
import os
import sys
import json
import urllib.request
import urllib.parse


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
}


class bing:
    origin = "https://cn.bing.com/HPImageArchive.aspx"

    items = []
    dates = []

    def __init__(self, datename) -> None:
        self.datename = datename

    def load(self):
        if os.path.exists(self.datename):
            with open(self.datename, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                date = item["date"]
                if date in self.dates:
                    continue
                self.dates.append(date)
                self.items.append(item)
        return self

    def dump(self):
        with open(self.datename, "w", encoding="utf-8") as f:
            json.dump(self.items, f)
        return self

    def sort(self):
        self.items.sort(key=lambda x: x['date'], reverse=True)
        return self

    def api(self, idx, n):
        params = {"format": "js", "idx": str(idx), "n": str(n)}
        url = self.origin + '?' + urllib.parse.urlencode(params)
        request = urllib.request.Request(url=url, headers=headers)
        reponse = urllib.request.urlopen(request, timeout=10)
        if 200 == reponse.status:
            data = reponse.read()
            for image in json.loads(data)["images"]:
                date = image["enddate"]
                if date in self.dates:
                    continue
                info = image["copyright"]
                url = "https://cn.bing.com" + image["urlbase"] + "_UHD.jpg"
                self.items.append({"date": date, "info": info, "url": url})
                print(date, info)
        else:
            print(reponse.status, reponse.url)
        return self

    def info(self, info):
        info = info.split("©")[0]
        if "(" == info[-1]:
            info = info[:-1]
        if "（" == info[-1]:
            info = info[:-1]
        while " " == info[-1]:
            info = info[:-1:]
        return info.replace('/', urllib.parse.quote('/', ''))

    def get(self, url, filename):
        state = False
        reponse = urllib.request.urlopen(url, timeout=10)
        if 200 == reponse.status:
            with open(filename, "wb") as f:
                f.write(reponse.read())
                state = True
        else:
            print(reponse.status, reponse.url)
        return state

    def download(self, prefix):
        if not os.path.exists(prefix):
            os.mkdir(prefix)
        for item in self.items:
            filename = prefix + '/' + item["date"] + '.jpg'
            if os.path.exists(filename):
                continue
            print("downloading...", end='\r')
            if self.get(item["url"], filename):
                print(item["date"], os.path.getsize(filename))
        return self


if "__main__" == __name__:
    datename = "data.json"
    if 1 < len(sys.argv):
        datename = sys.argv[1]
    b = bing(datename)
    b.load()
    b.api(0, 7).api(8, 8).sort()
    b.dump()
    if 2 < len(sys.argv):
        b.download(sys.argv[2])
