'''
Author: soonyenju@foxmail.com
Date: Jan. 06, 2019
'''

import os
from pathlib import Path
from spider import *


def main():
	'''
	Entrance to the whole project.
	'''

	spider = Spider()
	if not Path('../json/base_url.json').exists():
		spider.base_url()
	spider.hist_aqi('newaqi.json', stop_date = "20190101", provs = ['江苏'])
	# spider.easy_hist_aqi(date_range = ['201401', '201403'], prov_citys = {'安徽': ['合肥', '安庆']})

if __name__ == "__main__":
	main()
