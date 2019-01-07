# coding: utf-8
# from codes.config import Config
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import config
from logger import logger


class Spider(config.Config):
	"""
	Create a new spider
	"""

	def __init__(self):
		super(Spider, self).__init__()
		self.file_name = 'base_url.json'

	def base_url(self):
		'''
		To crawl the base url of each city, and saved the results as a json file named baseurl. 
		'''
		url_json = {}
		response = requests.get(self.url, headers=self.headers)
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
				aas = dd.find_all("a", href=True)
				for aa in aas:
					city_name = aa.get_text().strip()
					city_url = urljoin(self.url, aa["href"])
					url_json[prov_name][city_name] = city_url

		# with open("url.json", "w", encoding='utf-8') as f:
		# 	# indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
		# 	f.write(json.dumps(url_json, indent=4))
		with open(self.folder_json.joinpath(self.file_name), "w", encoding='utf-8') as f:
			json.dump(url_json, f, ensure_ascii=False, indent=4)

	def hist_aqi(self, name='aqi_.json', stop_date='20140101', provs=[]):
		stop_date = datetime.strptime(stop_date, r"%Y%m%d")
		with open(self.folder_json.joinpath(self.file_name), "r", encoding='utf-8') as f:
			base_urls = json.load(f)

		histaqi_data = {}

		if provs:
			keys = list(base_urls.keys())
			for key in keys:
				if key not in provs:
					base_urls.pop(key)

		for prov_name, city_urls in base_urls.items():
			histaqi_data[prov_name] = {}
			for city_name, city_url in city_urls.items():
				try:
					print(city_name, city_url)
					response = self.connect(city_url)
					html = response.text
					soup = BeautifulSoup(html, "lxml")
					boxs = soup.select("div.box.p")
					box = boxs[0]  # Box只有一个元素
					lis = box.select("li > a")
					city_data = {}
					for li in lis:
						city_mon_url = urljoin(city_url, li["href"])
						mon_name = li["title"]
						cur_date = datetime.strptime(
							mon_name[0:4] + mon_name[5:7], r"%Y%m")
						if (cur_date - stop_date).days < 0:
							break
						else:
							vals = self.interprter(city_mon_url)
							city_data[mon_name] = vals
							print(mon_name + " is done")
					histaqi_data[prov_name][city_name] = city_data
				except Exception as identifier:
					logger(self.log_path.joinpath('logging.log'), msg_type='error', msg=identifier)
					with open(datetime.now().strftime(r"%Y%m%d") + ".json", "w") as f:
						json.dump(histaqi_data, f,
								  ensure_ascii=False, indent=4)
					continue

		with open(self.folder_json.joinpath(name), "w", encoding='utf-8') as f:
			json.dump(histaqi_data, f, ensure_ascii=False, indent=4)

	def connect(self, url, encoding="gbk"):
		request_retry = requests.adapters.HTTPAdapter(
			max_retries=self.max_retries)
		s = requests.session()
		s.mount('https://', request_retry)
		s.mount('http://', request_retry)
		try:
			response = s.get(url, headers=self.headers, timeout=self.timeout)
		except Exception as identifier:
			print(identifier)
			time.sleep(5)
			response = s.get(url, headers=self.headers, timeout=self.timeout)
		response.encoding = encoding

		return response

	def interprter(self, city_mon_url):
		vals = []
		response = self.connect(city_mon_url)
		html = response.text
		soup = BeautifulSoup(html, "lxml")
		tds = soup.select("div.api_month_list td")
		for td in tds:
			if not td.attrs and not td.findChildren():
				item = td.get_text().strip()
				# print(item)
				vals.append(item)
		return vals

	def easy_hist_aqi(self, name ='easy_aqi.json', date_range = ['201301', '202001'], prov_citys = {'': []}):
		'''
		Usage:
		spider = Spider()
		spider.easy_hist_aqi(prov_citys = {'热门城市': [], '江苏': [], '安徽': ['合肥', '安庆']})
		spider.easy_hist_aqi(prov_citys = {'热门城市': ['北京', '天津']})
		'''
		stt_date = datetime.strptime(date_range[0], r"%Y%m")
		end_date = datetime.strptime(date_range[1], r"%Y%m")

		date_range = []
		while stt_date < end_date:
			date_range.append(stt_date.strftime(r"%Y%m"))
			stt_date += relativedelta(months=1)


		with open(self.folder_json.joinpath(self.file_name), "r", encoding='utf-8') as f:
			base_urls = json.load(f)

		histaqi_data = {}

		if prov_citys:
			temp_base_urls = {}
			for prov_name, city_names in prov_citys.items():
				temp_base_urls[prov_name] = {}
				if city_names:
					for city_name in city_names:
						temp_base_urls[prov_name][city_name] = base_urls[prov_name][city_name]
				else:
					temp_base_urls[prov_name] = base_urls[prov_name]

		base_urls = temp_base_urls
		del(temp_base_urls)

		for prov_name, city_urls in base_urls.items():
			histaqi_data[prov_name] = {}
			for city_name, city_url in city_urls.items():
				try:
					city_data = {}
					print(city_name)
					for mon_name in date_range:
						print(mon_name)
						city_mon_url = city_url.split('.html')[0] + '-' + mon_name + '.html'
						vals = self.interprter(city_mon_url)
						city_data[mon_name] = vals
						print(mon_name + " is done")
					histaqi_data[prov_name][city_name] = city_data

				except Exception as identifier:
					logger(self.log_path.joinpath('logging.log'), msg_type='error', msg=identifier)
					with open(datetime.now().strftime(r"%Y%m%d") + ".json", "w") as f:
						json.dump(histaqi_data, f,
								  ensure_ascii=False, indent=4)
					continue

		with open(self.folder_json.joinpath(name), "w", encoding='utf-8') as f:
			json.dump(histaqi_data, f, ensure_ascii=False, indent=4)
