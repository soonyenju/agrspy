import json
import numpy as np
import pandas as pd


def main():
	# preproc("20181218.json")

	with open('20181218.json', 'r', encoding='gbk') as f:
		histaqi = json.load(f)
	print('--------------------------------------')
	res = retrieve_data(histaqi)
	print('--------------------------------------')
	res = retrieve_data(histaqi, prov_name = '热门城市')
	print('--------------------------------------')
	res = retrieve_data(histaqi, prov_name = '热门城市', city_name = '成都')
	# print(res)
	print('--------------------------------------')
	print(res)


def retrieve_data(histaqi, prov_name = None, city_name = None):
	try:
		if city_name:
			city_data = histaqi[prov_name][city_name]
			results = fetch_data(city_data)
		else:
			results = {}
			for city_name, city_data in histaqi[prov_name].items():
				print(city_name)
				result = fetch_data(city_data)
				results[city_name] = result  
	except Exception as identifier:
		print(identifier)
		results = {}
		for prov_name, prov_data in histaqi.items():
			print(prov_name)
			results[prov_name] = {}
			for city_name, city_data in prov_data.items():
				print(city_name)
				result = fetch_data(city_data)
				results[prov_name][city_name] = result
	else:
		print(prov_name + " is done.")
	finally:
		return results


def fetch_data(city_data):
	result = []
	for val in city_data.values():
		result.extend(val)
	result = np.array(result).reshape(-1, 9)
	result = pd.DataFrame(result, columns = ['Date', 'aqi', 'aqi-rank', \
				'pm25', 'pm10', 'so2', 'no2', 'co', 'o3']).set_index('Date').sort_index()

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
			print(histaqi[prov_name])
			histaqi[prov_name][city_name.strip()] = histaqi[prov_name].pop(city_name)
	with open(filename, "w") as f:
		json.dump(histaqi, f, ensure_ascii = False, indent = 4)

if __name__ == "__main__":
	main()