import json
import numpy as np
import pandas as pd
from datetime import datetime

def main():
	preproc("aqi.json")
	exit(0)

	with open('aqi_jiangsu.json', 'r', encoding='gbk') as f:
		histaqi = json.load(f)
	# print('--------------------------------------')
	# res = retrieve_data(histaqi)
	# print('--------------------------------------')
	# res = retrieve_data(histaqi, prov_name = '热门城市')
	# print('--------------------------------------')
	# res = retrieve_data(histaqi, prov_name = '江苏', city_name = '南京')
	# print(res)
	# print('--------------------------------------')
	res = retrieve_data(histaqi)
	res = res['江苏']['南京']
	no2 = res.loc['2014-01-01':'2018-01-01', 'no2']


def retrieve_data(histaqi, prov_name = None, city_name = None):
	try:
		if city_name:
			print("fetching " + city_name)
			city_data = histaqi[prov_name][city_name]
			results = fetch_data(city_data)
		else:
			print("city name is not specified, fetching " + prov_name)
			results = {}
			for city_name, city_data in histaqi[prov_name].items():
				print(city_name)
				result = fetch_data(city_data)
				results[city_name] = result  
	except Exception as identifier:
		print(identifier)
		print("no name is specified, iterating...")
		results = {}
		for prov_name, prov_data in histaqi.items():
			print(prov_name)
			results[prov_name] = {}
			for city_name, city_data in prov_data.items():
				print(city_name)
				result = fetch_data(city_data)
				results[prov_name][city_name] = result
		print("iteration is done")
	else:
		print("retrieval is done.")
	finally:
		return results


def fetch_data(city_data):
	result = []
	for val in city_data.values():
		result.extend(val)
	result = np.array(result).reshape(-1, 9)
	result = pd.DataFrame(result, columns = ['Date', 'aqi', 'aqi-rank', \
				'pm25', 'pm10', 'so2', 'no2', 'co', 'o3'])

	result['Date'] = pd.to_datetime(result['Date']).sort_index()
	result.set_index("Date", inplace=True)
	result = pd.DataFrame(result, dtype=np.float)
	return result

def preproc(filename):
	'''
	去除city_name中的空格
	'''
	with open(filename, 'r', encoding='gbk') as f:
		histaqi = json.load(f)

	for prov_name, prov_data in histaqi.items():
		print(prov_name)
		for city_name in prov_data.keys():
			print(city_name)
			# print(histaqi[prov_name])
			histaqi[prov_name][city_name.strip()] = histaqi[prov_name].pop(city_name)
	with open(filename, "w") as f:
		json.dump(histaqi, f, ensure_ascii = False, indent = 4)

if __name__ == "__main__":
	main()