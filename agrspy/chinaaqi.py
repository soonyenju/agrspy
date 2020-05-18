from urllib.request import urlretrieve
import os, sys
from datetime import datetime, timedelta
import argparse

def hist_site_aqi(dates, path):
    base_url = 'https://quotsoft.net/air/data/china_sites_20151205.csv'
    for date in dates:
        url = base_url
        url = url.replace('20151205', date)
        # print(url)
        # print("*********************************************")
        print(date)
        try:
            urlretrieve(url, os.path.join(path, date + ".csv"), callbackfunc)
        except:
            pass
        # print("*********************************************")


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
    # print("%.2f%%"% percent)
    sys.stdout.write("%.2f%%\r"% percent)
    # sys.stdout.write(f"progress reaches {idx + 1} of {total}, {100*(idx + 1)/total}% ...\r")

if __name__ == "__main__":
    # main()
    parse = argparse.ArgumentParser()
    parse.add_argument("s", type = str, help = "start date")
    parse.add_argument("e", type = str, help = "end date")
    parse.add_argument("--path", type = str, help = "download directory", default = ".")
    args = parse.parse_args()
    s = args.s
    e = args.e
    dates, _, _ = cal_time(s = s, e = e)
    path = args.path
    hist_site_aqi(dates, path)

# how to use:
# python chinaaqi.py 20160101 20160103

# from agrspy import chinaaqi
# s = '20160101'
# e = '20160102'
# dates, _, _ = chinaaqi.cal_time(s = s, e = e)
# chinaaqi.hist_site_aqi(dates, ".")
