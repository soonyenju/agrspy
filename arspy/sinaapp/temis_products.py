# coding: utf-8
from __future__ import print_function
from __future__ import division
from datetime import *
import os, urllib
from urllib.request import *

def main():
    # path = r"F:\gome\gome"
    # dates, months, years  = cal_time()
    # gome_monthly(months, path)
    # path = r"F:\gome\scia"
    # dates, months, years  = cal_time(s = "20030101", e = "20120401")
    # scia_monthly(months, path)
    # path = r"F:\gome\gome2a"
    # dates, months, years  = cal_time(s = "20070101", e = "20140101")
    # gome2a_monthly(months, path)
    # path = r"F:\gome\gome2b"
    # dates, months, years  = cal_time(s = "20130101", e = "20160501")
    # gome2b_monthly(months, path)

    path = r"G:\no2"
    dates, months, years  = cal_time(s = "20041205", e = "20170101")
    omi_no2_daily(dates, path)




def omi_no2_daily(dates, path):
    base_url = "http://www.temis.nl/airpollution/no2col/data/omi/data_v2/2004/omi_no2_he5_20041001.tar"
    for date in dates:
        url = base_url
        url = url.replace(url[-12:-4],date)
        print(url)
        print("*********************************************")
        print(date)
        try:
            urlretrieve(url, os.path.join(path, date + ".tar"), callbackfunc)
        except:
            pass
        print("*********************************************")


def gome2b_monthly(months, path):
    gome2b_url = "http://h2co.aeronomie.be/ch2o/data/gome2b/v14/2013/01/GOME2BCH2O_Grid_720x1440_201301.dat"
    for month in months:
        url = gome2b_url
        url = url.replace(url[46: 53], month[0:4] + "/" + month[-2::])
        url = url.replace(url[-10: -4], month)
        print("*********************************************")
        print(month)
        try:
            urllib.request.urlretrieve(url, os.path.join(path, month + ".dat"), callbackfunc)
        except:
            pass
        print("*********************************************")

def gome2a_monthly(months, path):
    gome2a_url = "http://h2co.aeronomie.be/ch2o/data/gome2a/v14/2007/01/GOME2CH2O_Grid_720x1440_200701.dat"
    for month in months:
        url = gome2a_url
        url = url.replace(url[46: 53], month[0:4] + "/" + month[-2::])
        url = url.replace(url[-10: -4], month)
        print("*********************************************")
        print(month)
        try:
            urllib.request.urlretrieve(url, os.path.join(path, month + ".dat"), callbackfunc)
        except:
            pass
        print("*********************************************")

def scia_monthly(months, path):
    scia_url = "http://h2co.aeronomie.be/ch2o/data/scia/2003/01/SCIACH2O_Grid_720x1440_200301.dat"
    for month in months:
        url = scia_url
        url = url.replace(url[40: 47], month[0:4] + "/" + month[-2::])
        url = url.replace(url[-10: -4], month)
        print("*********************************************")
        print(month)
        try:
            urllib.request.urlretrieve(url, os.path.join(path, month + ".dat"), callbackfunc)
        except:
            pass
        print("*********************************************")

def gome_monthly(months, path):
    gome_url = "http://h2co.aeronomie.be/ch2o/data/gome/images_based/1997/01/GOMECH2O_Grid_360x720_199701.dat"
    for month in months:
        url = gome_url
        url = url.replace(url[53: 60], month[0:4] + "/" + month[-2::])
        url = url.replace(url[-10: -4], month)
        print("*********************************************")
        print(month)
        try:
            urllib.request.urlretrieve(url, os.path.join(path, month + ".dat"), callbackfunc)
        except:
            pass
        print("*********************************************")


def omi_hcho_daily(dates, path):
    base_url = "http://h2co.aeronomie.be/ch2o/data/omi/v14/OMIH2CO_Grid_720x1440_20041001.dat"
    for date in dates:
        url = base_url
        url = url.replace(url[-12:-4],date)
        print("*********************************************")
        print(date)
        try:
            urllib.request.urlretrieve(url, os.path.join(path, date + ".dat"), callbackfunc)
        except:
            pass
        print("*********************************************")



def cal_time(s = "19970101", e = "20030701"):
    start_date = datetime.strptime(s, "%Y%m%d")
    end_date = datetime.strptime(e, "%Y%m%d")
    delta = end_date - start_date
    dates = []
    months = []
    years = []
    for day in range(delta.days):
        step = timedelta(day)
        date_iter = datetime.strftime(start_date + step, "%Y%m%d")
        month_iter = datetime.strftime(start_date + step, "%Y%m")
        year_iter = datetime.strftime(start_date + step, "%Y")
        dates.append(date_iter)
        months.append(month_iter)
        years.append(year_iter)
    months = list(set(months))
    months.sort()
    years = list(set(years))
    years.sort()
    return dates, months, years


def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100: percent = 100
    print("%.2f%%"% percent)


if __name__ == '__main__':
    main()
    print("ok")