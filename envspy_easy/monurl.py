# coding: utf-8
import json
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from sylogger import logger


def main():
	run(stop_date = "20131101", provs = ['江苏'])

def run(stop_date = "20181101", provs = ['热门城市', '江苏']):
	stop_date = datetime.strptime(stop_date, r"%Y%m%d")
	histaqi_data = {}
	with open("url.json", "r", encoding='utf-8') as f:
		base_urls = json.load(f)
	
	keys = list(base_urls.keys())
	for key in keys:
		if key not in  provs:
			base_urls.pop(key)

	for prov_name, city_urls in base_urls.items():
		histaqi_data[prov_name] = {}
		for city_name, city_url in city_urls.items():
			try:
				print(city_name, city_url) 
				response = connect(city_url)
				html = response.text
				soup = BeautifulSoup(html, "lxml")
				boxs = soup.select("div.box.p")
				box = boxs[0] # Box只有一个元素
				lis = box.select("li > a")
				city_data = {}
				for li in lis:
					city_mon_url = urljoin(city_url, li["href"])
					mon_name = li["title"]
					print(mon_name)
					cur_date = datetime.strptime(mon_name[0:4] + mon_name[5:7], r"%Y%m")
					if (cur_date - stop_date).days < 0:
						break
					else:
						vals = read(city_mon_url)
						city_data[mon_name] = vals
						print(mon_name + " is done")
				histaqi_data[prov_name][city_name] = city_data
				# print(histaqi_data)
			except Exception as identifier:
				logger('logging.log', msg_type='error', msg=identifier)
				with open(datetime.now().strftime(r"%Y%m%d") + ".json", "w") as f:
					json.dump(histaqi_data, f, ensure_ascii = False, indent = 4)
				continue


	with open("aqi.json", "w") as f:
		json.dump(histaqi_data, f, ensure_ascii = False, indent = 4)


# https://www.cnblogs.com/kongzhagen/p/6472746.html
# https://www.biaodianfu.com/python-requests-retry.html
# https://blog.csdn.net/xie_0723/article/details/52790786
def read(city_mon_url):
	vals = []
	response = connect(city_mon_url)
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	tds = soup.select("div.api_month_list td")
	for td in tds:
		if not td.attrs and not td.findChildren():
			item = td.get_text().strip()
			# print(item)
			vals.append(item)
	# exit(0)
	return vals 

def connect(url, timeout = 500, max_retries = 30, encoding = "gbk"):
	headers = {'user-agent': 'my-app/0.0.1'}
	request_retry = requests.adapters.HTTPAdapter(max_retries = max_retries)
	s = requests.session()
	s.mount('https://',request_retry)  
	s.mount('http://',request_retry)
	try:
		response = s.get(url, headers = headers, timeout = timeout)
	except Exception as identifier:
		print(identifier)
		time.sleep(5)
		response = s.get(url, headers = headers, timeout = timeout)	
	response.encoding = encoding

	return response


if __name__ == "__main__":
	main()
