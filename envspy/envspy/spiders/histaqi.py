# -*- coding: utf-8 -*-
import scrapy
import json
from envspy.items import EnvspyItem


class HistaqiSpider(scrapy.Spider):
	name = 'histaqi'
	allowed_domains = ['www.tianqihoubao.com/aqi']
	start_urls = ['http://www.tianqihoubao.com/aqi/']

	def parse(self, response):
		item = EnvspyItem()
		with open("baseurl.json", "r", encoding='gbk') as f:
			base_urls = json.load(f)
		item["baseurls"] = base_urls
		for prov_name, prov in base_urls.items():
			# print(prov_name) 
			for city_name, city_url in prov.items():
				# print(city_name)
				abs_city_url = response.urljoin(city_url)
				yield scrapy.Request(abs_city_url, meta = {'item': item, 'prov_city': [prov_name, city_name]}, callback=self.crawl_histaqi, dont_filter=True)
				# exit(0)
		# print(item["baseurls"])
		# print(item)
		# exit(0)

	# https://www.jianshu.com/p/de61ed0f961d
	def crawl_histaqi(self, response):
		hist_table = response.xpath('//*[@id="bd"]/div[1]/div[3]/ul')[0]
		hists = hist_table.xpath('.//li')
		item = response.meta['item']
		# base_urls = item['baseurls']
		prov_name, city_name = response.meta['prov_city']
		# print(response.meta['prov_city'])
		hist_urls = {}
		for hist in hists:
			title = hist.xpath('a/@title').extract_first()
			title = bytes(title, encoding = response.encoding).decode("gbk")
			hist_url = hist.xpath('a/@href').extract_first()
			hist_url = response.urljoin(hist_url)
			hist_urls[title] = hist_url
			yield scrapy.Request(hist_url, meta = {'item': item, 'prov_city': [prov_name, city_name]}, callback=self.fetch_data, dont_filter=True)
			# exit(0)
		return item
	
	def fetch_data(self, response):
		print("fetching data...")
		vals = []
		prov_name, city_name = response.meta['prov_city']
		print(prov_name, city_name)
		item = response.meta['item']
		trs = response.xpath('//*[@id="content"]/div[3]')[0].xpath('table')[0].xpath('tr')
		for tr in trs:
			tds = tr.xpath('.//td/text()')
			for td in tds:
				val = td.extract().strip()
				vals.append(val)
		item['baseurls'][prov_name][city_name] = vals
		print("fetch done.")
		return item
