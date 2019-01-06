from urllib.request import urlretrieve
import os
from datetime import datetime, timedelta

def main():
    path = r"D:\no2"
    print('ok')
    dates, _, _ = cal_time(s = '20140101', e = '20190101')
    hist_site_aqi(dates, path)

def hist_site_aqi(dates, path):
    base_url = 'http://beijingair.sinaapp.com/data/china/sites/20151205/csv'
    for date in dates:
        url = base_url
        url = url.replace('20151205',date)
        print(url)
        print("*********************************************")
        print(date)
        try:
            urlretrieve(url, os.path.join(path, date + ".csv"), callbackfunc)
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

if __name__ == "__main__":
    main()