# -*- coding: utf-8 -*-
import scrapy, re, time
import json
from datetime import datetime
from envspy.items import EnvspyItem


class HistaqiSpider(scrapy.Spider):
	name = 'nrtaqi'
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
				yield scrapy.Request(abs_city_url, callback=self.crawl_nrtaqi, dont_filter=True)
				# exit(0)
		# print(item["baseurls"])
		# print(item)
		# exit(0)

	# https://www.jianshu.com/p/de61ed0f961d
	def crawl_nrtaqi(self, response):
		print(response.url)
		print('ok')
		minute = int(datetime.now().strftime(r"%M"))
		if minute >= 48: 
			print("stop")
			return 0
		table = response.xpath('//*[@id="content"]/div[4]/table')
		tds = table.xpath('.//td/text()').extract()
		vals = []
		for td in tds:
			vals.append(td.strip())
		timetag = response.xpath('//*[@id="content"]/div[1]/text()').extract_first().strip()
		h1 = response.xpath('//*[@id="content"]/h1/text()').extract_first().strip()
		timetag = re.findall(r'\d+-\d+-\d+', timetag)[0]
		# '2018-12-20'
		out = ''.join(re.findall(r'[\u4E00-\u9FA5]', h1))
		idx = out.index(re.findall(r'[\u4E00-\u9FA5]' + '空气', h1)[0][0])
		name = out[0: idx+1] + '-' + timetag
		print(name,vals)
		if ''.join(vals):
			print("lalalal")
			time.sleep(5)
			yield scrapy.Request(response.url, callback=self.crawl_nrtaqi, dont_filter=True)
		else:
			with open(name + ".json", "w") as f:
				json.dump({name: vals}, f, ensure_ascii=False, indent=4)

