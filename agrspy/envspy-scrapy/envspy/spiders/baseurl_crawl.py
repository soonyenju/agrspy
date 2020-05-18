# -*- coding: utf-8 -*-
import scrapy
import json


class HistaqiSpider(scrapy.Spider):
    name = 'baseurl_crawl'
    allowed_domains = ['http://www.tianqihoubao.com/aqi']
    start_urls = ['http://www.tianqihoubao.com/aqi/']

    def parse(self, response):
        print("starting...")
        base_url_json = {}
        provs = response.xpath('//*[@id="content"]/div[2]')[0].xpath('.//dl')
        for prov in provs:
            cities = prov.xpath('dd').xpath('.//a')
            prov_name = prov.xpath('dt/b/text()').extract_first()
            prov_name = bytes(prov_name, encoding = response.encoding).decode("gbk")
            base_url_json[prov_name] = {}
            for city in cities:
                try:
                    city_name = city.xpath('text()').extract_first()
                    city_name = bytes(city_name, encoding = response.encoding).decode("gbk")
                    city_url = city.xpath('@href').extract_first()
                    base_url_json[prov_name][city_name] = city_url
                except Exception as e:
                    # print(e)
                    continue

        # with open("url.json", "w", encoding='utf-8') as f:
        # 	# indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
        with open("baseurl.json", "w") as f:
            json.dump(base_url_json, f, ensure_ascii = False, indent = 4)
        print("done")

