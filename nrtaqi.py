# coding: utf-8
import json
import time
from datetime import datetime
from urllib.parse import urljoin

import numpy as np
import requests
from bs4 import BeautifulSoup


def main():
	# process the dowloaded data
	with open("nrtaqi.json", "r", encoding='gbk') as f:
		nrtaqi = json.load(f)
	for prov_name, prov in nrtaqi.items():
		for city_name, city in prov.items():
			city = np.array(city).reshape(-1, 9)
			timestamp = datetime.now().strftime("%Y-%m-%d:%H")
			if not (isinstance(nrtaqi, dict) and timestamp in nrtaqi.keys()):
				nrtaqi[prov_name][city_name] = {timestamp: city}
	print(nrtaqi)
			# exit(0)

def run():
	headers = {'user-agent': 'my-app/0.0.1'}
	with open("url.json", "r", encoding='utf-8') as f:
		base_urls = json.load(f)

	result = {}	
	for prov_name, city_urls in base_urls.items():
		result[prov_name] = {}
		for city_name, city_url in city_urls.items():
			print(city_name, city_url)
			response = requests.get(city_url, headers=headers)
			response.encoding = "gbk"
			html = response.text
			soup = BeautifulSoup(html, "lxml")
			tbodies = soup.find_all("td")
			result[prov_name][city_name] = []
			for tbody in tbodies:
				result[prov_name][city_name].append(tbody.get_text().strip())
			time.sleep(0.01)
		print(result)
		with open("nrtaqi.json", "w") as f:
			json.dump(result, f, ensure_ascii=False, indent=4)
		exit(0)




if __name__ == "__main__":
	main()
