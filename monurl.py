# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def main():
	headers = {'user-agent': 'my-app/0.0.1'}
	with open("url.json", "r", encoding='utf-8') as f:
		base_urls = json.load(f)

	for prov_name, city_urls in base_urls.items():
		for city_name, city_url in city_urls.items():
			print(city_name, city_url) 
			response = requests.get(city_url, headers = headers)
			response.encoding = "gbk"
			html = response.text
			soup = BeautifulSoup(html, "lxml")
			boxs = soup.select("div.box.p")
			for box in boxs:
				lis = box.select("li > a")
				for li in lis:
					city_mon_url = urljoin(city_url, li["href"])
					print(li["title"])
					print(city_mon_url)
					read(city_mon_url)
					exit(0)
			exit(0)

# https://www.cnblogs.com/kongzhagen/p/6472746.html
def read(city_mon_url):
	headers = {'user-agent': 'my-app/0.0.1'}
	response = requests.get(city_mon_url, headers = headers)
	response.encoding = "gbk"
	html = response.text
	soup = BeautifulSoup(html, "lxml")
	tds = soup.select("div.api_month_list td")
	for td in tds:
		if not td.attrs and not td.findChildren():
			item = td.get_text().strip()
			print(item)
	# exit(0)


if __name__ == "__main__":
	main()

