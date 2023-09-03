#
#
#
#
# Company -> Scania
# Link ----> https://www.scania.com/ro/ro/home/about-scania/career/available-positions.html
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class ScaniaSpiderSpider(scrapy.Spider):
    name = "scania_spider"
    allowed_domains = ["www.scania.com"]
    start_urls = ["https://www.scania.com/ro/ro/home/about-scania/career/available-positions.html"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for link in response.css('a.cmp-list__item-link::attr(href)').extract():
            yield scrapy.Request('https://www.scania.com' + link, callback=self.parse_job)

    def parse_job(self, response):
        if (data := response.css('p > b::text').get()):
            if 'location' in data.lower() or 'locatie' in data.lower():

                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = response.url
                item['job_title'] = response.css('h2.cmp-title__text::text').get().capitalize()
                item['company'] = 'Scania'
                item['country'] = 'Romania'
                item['city'] = response.css('p > b::text').get().split()[-1].replace(',', '')
                item['logo_company'] = 'https://www.scania.com/content/dam/scanianoe/market/master/homepage/scania-wordmark.svg'
                #
                yield item
