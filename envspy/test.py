# coding: utf-8
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import urllib
import requests

def main():
    headers = {'user-agent': 'my-app/0.0.1'}
    url = 'http://www.tianqihoubao.com/aqi/'
    response = requests.get(url, headers = headers)
    response.encoding = 'gbk'
    soup = BeautifulSoup(response.text, features="lxml")
    dls = soup.find_all("dl")
    for i, dl in enumerate(dls):
        # print(dl)
        # print(dir(dl))
        # print(i)
        dts = dl.find_all("dt")
        # for dt in dts:
        #     print(dt.get_text())
        dds = dl.find_all("dd")[0]
        for dd in dds:
            try:
                print(dd.get_text())
                print(dd.get("href"))
                if dd.find_all("wbr"):
                    print("11111111111111111")
                print(dd)
            except Exception as identifier:
                print(identifier)
            # print(dd.get_text())
            # print(dd.get("href"))
            # print(dir(dd))
            # print(dd)
            # print(dd.get("href"))
            # exit(0)


if __name__ == "__main__":
    main()
    pass
