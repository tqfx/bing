#!/usr/bin/env python
# -*- coding : utf-8 -*-
import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
}


class bing:
    origin = "https://cn.bing.com/HPImageArchive.aspx"

    items = []
    dates = []
    w404 = []
    t404 = []

    def __init__(self, prefix) -> None:
        self.prefix = os.path.relpath(prefix)
        if not os.path.exists(self.prefix):
            os.mkdir(self.prefix)

    def load(self):
        if os.path.exists(self.prefix + "/.w404.json"):
            with open(self.prefix + "/.w404.json", "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                date = item["date"]
                if date in self.dates or date in self.w404:
                    continue
                self.t404.append(date)
                self.w404.append(item)
        if os.path.exists(self.prefix + "/.data.json"):
            with open(self.prefix + "/.data.json", "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                date = item["date"]
                if date in self.dates or date in self.t404:
                    continue
                self.dates.append(date)
                self.items.append(item)
        return self

    def dump(self):
        self.items.sort(key=lambda x: x['date'], reverse=True)
        with open(self.prefix + "/.data.json", "w", encoding="utf-8") as f:
            json.dump(self.items, f)
        return self

    def werr(self):
        self.w404.sort(key=lambda x: x['date'], reverse=True)
        with open(self.prefix + "/.w404.json", "w", encoding="utf-8") as f:
            json.dump(self.w404, f)
        return self

    def api(self, idx, n):
        params = {"format": "js", "idx": str(idx), "n": str(n)}
        url = self.origin + '?' + urllib.parse.urlencode(params)
        request = urllib.request.Request(url=url, headers=headers)
        try:
            reponse = urllib.request.urlopen(request, timeout=10)
            data = reponse.read()
            for image in json.loads(data)["images"]:
                date = image["enddate"]
                if date in self.dates:
                    continue
                info = image["copyright"]
                url = "https://cn.bing.com" + image["urlbase"] + "_UHD.jpg"
                self.items.append({"date": date, "info": info, "url": url})
                print(date, info)
        except urllib.error.HTTPError as e:
            print(e.code, e.url)
        except Exception as e:
            print(e)
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

    def get(self, item, filename):
        state = False
        try:
            reponse = urllib.request.urlopen(item["url"])
            with open(filename, "wb") as f:
                f.write(reponse.read())
                state = True
        except urllib.error.HTTPError as e:
            if 404 == e.code:
                self.w404.append(item)
        except urllib.error.URLError as e:
            print(e)
        except Exception as e:
            print(e)
        return state

    def download(self):
        for item in self.items:
            filename = self.prefix + '/' + item["date"] + '.jpg'
            if os.path.exists(filename):
                continue
            print(item["date"] + "...", end='\r')
            if self.get(item, filename):
                print(filename)
        self.werr()
        return self


if "__main__" == __name__:
    prefix = "image"
    if 1 < len(sys.argv):
        prefix = sys.argv[1]
    b = bing(prefix)
    b.load()
    b.api(0, 7).api(8, 8)
    b.dump()
    if 1 < len(sys.argv):
        b.download()
    b.dump()
