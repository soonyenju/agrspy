# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json, time

def main():
	histaqi_data = {}
	with open("url.json", "r", encoding='utf-8') as f:
		base_urls = json.load(f)

	for prov_name, city_urls in base_urls.items():
		histaqi_data[prov_name] = {}
		for city_name, city_url in city_urls.items():
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
				vals = read(city_mon_url)
				city_data[mon_name] = vals
				print(mon_name)
			histaqi_data[prov_name][city_name] = city_data
			# print(histaqi_data)


	# with open("url.json", "w", encoding='utf-8') as f:
	# 	# indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
	# 	f.write(json.dumps(url_json, indent=4))
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

