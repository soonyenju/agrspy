'''
Author: soonyenju@foxmail.com
Date: Jan. 06, 2019
'''

import os
from pathlib import Path
from spider import *
from postproc import *


def main():
	'''
	Entrance to the whole project.
	'''
	postor = Postor('../json/aqi.json')
	# postor.merger('../json/newaqi.json', replace = True)
	# postor.batch_json2csv()
	with open(postor.hub_path, 'r', encoding='utf-8') as f:
		histaqi = json.load(f)
	prov_dfs = postor.retrieve_data(histaqi)
	res = prov_dfs['江苏']['南京']
	no2 = res.loc['2014-01-01':'2018-12-31', 'no2']
	print(no2)


def iterate_json():
	with open('../json/aqi.json', "r", encoding='utf-8') as f:
		aqi = json.load(f)
	for prov_name, prov_data in aqi.items():
		print(prov_name)
		for city_name, city_data in prov_data.items():
			print(city_name)
			for mon_name, mon_data in city_data.items():
				print(mon_name) 


def crawling():
	spider = Spider()
	if not Path('../json/base_url.json').exists():
		spider.base_url()
	# spider.hist_aqi('newaqi.json', stop_date = "20190101", provs = ['江苏'])
	# spider.easy_hist_aqi(date_range = ['201401', '201403'], prov_citys = {'安徽': ['合肥', '安庆']})



if __name__ == "__main__":
	main()
