import scrapy
from bs4 import BeautifulSoup as bs

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.tianqihoubao.com/aqi/',
    ]

    def parse(self, response):
        print("fine")
        print(type(response))
        body = response.body
        soup = bs(body, features="lxml")
        cities = soup.find_all("dl")
        print(cities)
        print("ok")
        exit(0)
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").extract_first(),
                "author": quote.xpath("span/small/text()").extract_first(),
            }
        next_page = response.css("li.next a::attr('href')").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
