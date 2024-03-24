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
        for link in response.xpath('//a[@class="cmp-list__item-link"]/@href').extract():
            yield scrapy.Request('https://www.scania.com' + link, callback=self.parse_job)

    def parse_job(self, response):

        # get location from Scania
        if (location := [elem.lower() for elem\
                    in response.xpath('//div[@class="cmp-text"]//p//text()').extract()\
                        if 'locatie' in elem.lower()]):
            locations = [city.strip().title() for city in location[0].split('scania')[1:] if city.strip()]
            # get items with new locations
            item = JobItem()
            item['job_link'] = response.url
            item['job_title'] = response.css('h2.cmp-title__text::text').get().capitalize()
            item['company'] = 'Scania'
            item['country'] = 'Romania'
            item['county'] = ''
            item['city'] = locations[0] if len(locations) == 1 else locations
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://www.scania.com/content/dam/scanianoe/market/master/homepage/scania-wordmark.svg'
            #
            yield item
