#!/usr/bin/env python3
# -*- coding : utf-8 -*-
import os
import re
import time
import json
import sys
from urllib.parse import quote, unquote

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


def char_path(text, mode=False):
    """
    brief: 处理非法路径字符 \n
    param: text 路径字符串 \n
    param: mode False 转码 True 解码 \n
    return: 处理后的字符串\n
    """
    text = str(text)
    if "%" in text:
        text = unquote(text)
    if mode:
        return text
    tuple_char = ("\\", ":", "*", "?", '"', "<", ">", "|")
    for char in tuple_char:
        text = text.replace(char, quote(char))
    return text


def dealname(name):
    """
    brief: 处理信息\n
    param: name 信息\n
    return: 处理后的信息\n
    """
    name = str(name).split("©")[0]
    if "(" == name[-1]:
        name = name[:-1:]
    if "（" == name[-1]:
        name = name[:-1:]
    while " " == name[-1]:
        name = name[:-1:]
    return name


def mkdir(pwd):
    try:
        os.mkdir(pwd)
    except FileNotFoundError:
        os.makedirs(pwd)
    except FileExistsError:
        pass
    return


def download(url, filename, pwd):
    if "/" != pwd[-1]:
        pwd += "/"

    filename = char_path(filename)
    filename = filename.replace("/", quote("/", ""))

    print("log:", url, "downloading")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    http = urllib3.PoolManager()
    response = http.request("GET", url, headers=headers)
    with open(pwd + filename, "wb") as f:
        f.write(response.data)
    response.release_conn()

    print("已下载 {}".format(filename))


def html_deal(text, url, pwd):
    soup = BeautifulSoup(text, "html.parser")

    bstag = soup.find_all("div", id="bgImgProgLoad")
    if bstag == []:
        print("error:", "bs4 div bgImgProgLoad")
    else:
        src = re.findall('src="([^&]*)', str(bstag))[0]
        if "/" in url[-1]:
            src = url[:-1:] + src
        else:
            src = url + src
    del bstag

    titletag = soup.find_all("a", id="sh_cp")
    if titletag == []:
        print("error:", "bs4 a sh_cp")
    else:
        name = re.findall('title="([^"]*)"', str(titletag))[0]
        info = name
        name = dealname(name)
    del titletag

    del soup

    t = time.strftime("%Y%m%d", time.localtime())
    if "/" != pwd[-1]:
        pwd += "/"
    pwd += t + "/"
    mkdir(pwd)

    filename = name + ".jpg"
    if filename in os.listdir(pwd):
        print("warning:", "{} exists!".format(filename))
    else:
        download(src, filename, pwd)
    del filename

    infodict = {"info": info, "date": t, "src": src}
    del t
    del info
    del src

    mp4list = re.findall(r'"\\/\\/([^"]*)"', text)
    if mp4list != []:
        srcset = set()
        for i in range(len(mp4list)):
            mp4list[i] = "https://" + mp4list[i].replace("\\", "")
            srctag = mp4list[i].split("_")[1]
            if srctag in srcset:
                mp4list[i] = ""
            else:
                srcset.add(srctag)
            del srctag
        mp4list.remove("")
        del srcset

    for src in mp4list:
        filename = name + "_" + src.split("_")[1] + ".mp4"
        infodict[src.split("_")[1]] = src
        del filename
    del mp4list

    return infodict


def html_get(pwd, url="https://cn.bing.com/"):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }

    r = requests.get(url, headers=headers, timeout=5)

    r.encoding = r.apparent_encoding
    print("log:", r.url, r.status_code)

    if r.status_code == 200:
        return html_deal(r.text, url, pwd)

    return dict()


def api_deal(text, pwd):
    list_out = []
    list_img = json.loads(text)["images"]
    for dict_img in list_img:
        src = "https://cn.bing.com" + dict_img["urlbase"] + "_UHD.jpg"
        date = dict_img["enddate"]
        info = dict_img["copyright"]
        mkdir(pwd + date)
        filename = dealname(info) + ".jpg"
        if filename not in os.listdir(pwd + date):
            download(src, filename, pwd + date + "/")
            list_out.append({"info": info, "date": date, "src": src})
    return list_out


def api_get(pwd, url="https://cn.bing.com/HPImageArchive.aspx"):
    if "/" != pwd[-1]:
        pwd += "/"
    list_out = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }

    params = {"format": "js", "idx": "0", "n": "7"}

    r = requests.get(url, headers=headers, params=params, timeout=5)

    r.encoding = r.apparent_encoding
    print("log:", r.url, r.status_code)

    if r.status_code == 200:
        list_out += api_deal(r.text, pwd)

    params = {"format": "js", "idx": "8", "n": "8"}

    r = requests.get(url, headers=headers, params=params, timeout=5)

    r.encoding = r.apparent_encoding
    print("log:", r.url, r.status_code)

    if r.status_code == 200:
        list_out += api_deal(r.text, pwd)

    return list_out


def bin(pwd, data="bing.json"):
    try:
        with open(data, "r", encoding="utf-8") as f:
            inlist = json.load(f)
    except:
        inlist = []

    dict_img = html_get(pwd)
    if dict_img != dict():
        inlist.append(dict_img)
    inlist += api_get(pwd)

    inlist = sorted(inlist, key=lambda img: img["date"], reverse=True)
    with open(data, "w", encoding="utf-8") as f:
        json.dump(inlist, f)

    return


if __name__ == "__main__":
    try:
        pwd = sys.argv[1]
    except:
        pwd = "img"

    bin(pwd)
    while 3 > len(sys.argv):
        t1 = time.strftime("%H%M%S", time.localtime())
        if t1 == "000000":
            bin(pwd)
        print(time.ctime(), end="\r")
        time.sleep(1)
