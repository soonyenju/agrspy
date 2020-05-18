import os, json
import config

import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path


class Postor(config.Config):
	"""
	Create a new postor
	"""

	def __init__(self, hub_path):
		super(Postor, self).__init__()
		self.hub_path = hub_path

	def merger(self, new_path, out_name = 'merged.json', replace = False):
		# 改用dict.update()方法！！		
		with open(self.hub_path, "r", encoding='utf-8') as f:
			aqi_hub = json.load(f)

		with open(new_path, "r", encoding='utf-8') as f:
			aqi_new = json.load(f)

		for prov_name, prov_data in aqi_new.items():
			print(prov_name)
			for city_name, city_data in prov_data.items():
				print(city_name)
				if not city_name in aqi_hub[prov_name].keys():
					aqi_hub[prov_name][city_name] = {}
				for mon_name, mon_data in city_data.items():
					print(mon_name)
					if mon_name in aqi_hub[prov_name][city_name].keys():
						if replace == True:
							aqi_hub[prov_name][city_name][mon_name] = aqi_new[prov_name][city_name][mon_name]
					else:
						aqi_hub[prov_name][city_name][mon_name] = aqi_new[prov_name][city_name][mon_name]
		with open(self.folder_json.joinpath(out_name), "w", encoding='utf-8') as f:
			json.dump(aqi_hub, f, ensure_ascii=False, indent=4)


	def batch_json2csv(self, prov_name = None, city_name = None):
		with open(self.hub_path, 'r', encoding='utf-8') as f:
			histaqi = json.load(f)

		aqi_dfs = self.retrieve_data(histaqi, prov_name = prov_name, city_name = city_name)

		for prov_name, prov_data in aqi_dfs.items():
			prov_path = self.folder_csv.joinpath(prov_name)
			if not prov_path.exists():
				os.makedirs(prov_path)
			for city_name, city_data in prov_data.items():
				csv_name = prov_path.joinpath(city_name + '.csv')
				if not os.path.exists(csv_name.as_posix()): city_data.to_csv(csv_name)
				print(f'{prov_name}: {city_name} is successfully transferred to csv.')


	def retrieve_data(self, histaqi, prov_name = None, city_name = None):
		try:
			if city_name:
				print("fetching " + city_name)
				city_data = histaqi[prov_name][city_name]
				results = self.fetch_data(city_data)
			else:
				print("city name is not specified, fetching " + prov_name)
				results = {}
				for city_name, city_data in histaqi[prov_name].items():
					print(city_name)
					result = self.fetch_data(city_data)
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
					result = self.fetch_data(city_data)
					results[prov_name][city_name] = result
			print("iteration is done")
		else:
			print("retrieval is done.")
		finally:
			return results

	def fetch_data(self, city_data):
		result = []
		for val in city_data.values():
			result.extend(val)
		result = np.array(result).reshape(-1, 9)
		result = pd.DataFrame(result, columns = ['Date', 'aqi', 'aqi-rank', \
					'pm25', 'pm10', 'so2', 'no2', 'co', 'o3'])

		result['Date'] = pd.to_datetime(result['Date']).sort_index()
		result.set_index("Date", inplace=True)
		result = pd.DataFrame(result, dtype=np.float).sort_index()
		return result

	def eliminate_spaces(self):
		'''
		去除city_name中的空格
		'''
		with open(self.hub_path, 'r', encoding='utf-8') as f:
			histaqi = json.load(f)

		for prov_name, prov_data in histaqi.items():
			print(prov_name)
			for city_name in prov_data.keys():
				print(city_name)
				# print(histaqi[prov_name])
				histaqi[prov_name][city_name.strip()] = histaqi[prov_name].pop(city_name)
		with open(self.hub_path, "w") as f:
			json.dump(histaqi, f, ensure_ascii = False, indent = 4)