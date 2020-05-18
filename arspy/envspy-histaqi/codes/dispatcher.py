'''
Author: soonyenju@foxmail.com
Date: Jan. 07, 2019
'''

import os
import pickle
from pathlib import Path

from postproc import *
from spider import *

from datetime import datetime, timedelta


def main():
	'''
	Entrance to the whole project.
	'''
	postor = Postor('../json/aqi.json')
	# postor.merger('../json/newaqi.json', replace = True)
	# postor.batch_json2csv()

	# dump2pkl(postor)

	stt_date = '2014-01-01'
	end_date = '2018-12-31'
	sd = datetime.strptime(stt_date, r"%Y-%m-%d")
	ed = datetime.strptime(end_date, r"%Y-%m-%d")
	date_range = []
	while sd <= ed:
		date_range.append(sd)
		sd += timedelta(days=1)
	# print(date_range)
	with open('yrd.pkl', 'rb') as f:
		dfs = pickle.load(f)
	for prov_name, prov_data in dfs.items():
		print(prov_name)
		for city_name, city_data in prov_data.items():
			print(city_name)
			'''
			no2 = city_data.loc[stt_date: end_date, 'no2']
			for date in date_range:
				if date not in no2.index:
					no2[date] = None
			no2 = no2.sort_index()
			print(no2)
			'''
			aqi = city_data.loc[stt_date: end_date]
			newline = pd.DataFrame(
				[None, None, None, None, None, None, None, None]).T
			newline.columns = aqi.columns
			missing_date = []
			for date in date_range:
				if date not in aqi.index:
					missing_date.append(date)

			missing_df = pd.DataFrame(np.empty([len(missing_date), len(aqi.columns)], dtype=object),
									  columns=aqi.columns,
									  index=missing_date)
			aqi = pd.concat([aqi, missing_df])
			aqi = aqi.sort_index()

			out_folder = Path.cwd().parent.joinpath('formated_csv').joinpath(prov_name)
			if not out_folder.exists():
				os.makedirs(out_folder)
			csv_name = out_folder.joinpath(city_name + '.csv')
			if not os.path.exists(csv_name.as_posix()): aqi.to_csv(csv_name)
			print(f'{prov_name}: {city_name} is successfully formatted.')
			# exit(0)

	# res = prov_dfs['江苏']['南京']
	# no2 = res.loc['2014-01-01':'2018-12-31', 'no2']
	# print(no2)


def dump2pkl(postor):
	keys = ['江苏', '浙江', '上海', '山东', '安徽']
	with open(postor.hub_path, 'r', encoding='utf-8') as f:
		histaqi = json.load(f)
	prov_dfs = postor.retrieve_data(histaqi)
	prov_dfs['上海'] = {}
	prov_dfs['上海']['上海'] = prov_dfs['热门城市']['上海']
	df_out = {}
	for key in keys:
		df_out[key] = prov_dfs[key]
	with open('yrd.pkl', 'wb') as f:
		pickle.dump(df_out, f)


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
