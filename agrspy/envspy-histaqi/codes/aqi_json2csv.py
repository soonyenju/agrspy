# coding: utf-8
import os, json
from pathlib import Path
from xpinyin import Pinyin
import numpy as np
import pandas as pd

def main():
	P = Pinyin()
	with open('aqi.json', 'r', encoding='utf-8') as f:
		aqi = json.load(f)

	for key in aqi.keys():
		print(key)
		prov_name = P.get_pinyin(key, '').capitalize()
		prov_name_path = Path.cwd().joinpath('aqi').joinpath(prov_name)
		# if not prov_name_path.exists(): prov_name_path.mkdir()
		# print(prov_name_path)
		if not os.path.exists(prov_name_path.as_posix()): os.makedirs(prov_name_path.as_posix())

		for city_name, city_values in aqi[key].items():
			print(city_name)
			city_list = []
			for cv in city_values.values():
				city_list.extend(cv)
			city_list = pd.DataFrame(np.array(city_list).reshape(-1, 9), columns = ['date', 'aqi', 'aqi_rank', 'pm25', 'pm10', 'so2', 'no2', 'co', 'o3']).set_index('date')
			csv_name = prov_name_path.joinpath(city_name + '.csv')
			if not os.path.exists(csv_name.as_posix()): city_list.to_csv(csv_name)
			
 

if __name__ == "__main__":
	main()