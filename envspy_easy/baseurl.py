# coding: utf-8
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

def main():
	url_json = {}
	url = "http://www.tianqihoubao.com/aqi/"
	headers = {'user-agent': 'my-app/0.0.1'}
	response = requests.get(url, headers = headers)
	response.encoding = "gbk"
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	dls = soup.find_all("dl")
	for dl in dls:
		dts = dl.find_all("dt")
		for dt in dts:
			prov_name = dt.get_text()
			url_json[prov_name] = {}
		dds = dl.find_all("dd")
		for dd in dds:
			aas = dd.find_all("a", href = True)
			for aa in aas:
				city_name = aa.get_text().strip()
				city_url = urljoin(url, aa["href"])
				url_json[prov_name][city_name] = city_url

	# with open("url.json", "w", encoding='utf-8') as f:
	# 	# indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
	# 	f.write(json.dumps(url_json, indent=4))
	with open("url.json", "w") as f:
		json.dump(url_json, f, ensure_ascii = False, indent = 4)



if __name__ == "__main__":
	main()
	pass