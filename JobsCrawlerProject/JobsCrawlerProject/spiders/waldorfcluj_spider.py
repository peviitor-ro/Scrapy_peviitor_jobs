#
#
#
#
# Company -> WaldorfCluj
# Link ----> https://waldorfcluj.ro/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class WaldorfclujSpiderSpider(scrapy.Spider):
    name = "waldorfcluj_spider"
    allowed_domains = ["waldorfcluj.ro"]
    start_urls = ["https://waldorfcluj.ro/"]

    def parse(self, response):
        
        if (response_jobs := response.xpath('//ul[@class="has-normal-font-size"]')):
            for job in response_jobs:
                title = job.xpath('.//li//strong//text()').extract_first()
                #
                if title:
                    item = JobItem()
                    item['job_link'] = job.xpath('.//li/a/@href').extract_first()
                    item['job_title'] = title
                    item['company'] = 'WaldorfCluj'
                    item['country'] = 'Romania'
                    item['county'] = 'Cluj'
                    item['city'] = 'Cluj-Napoca'
                    item['remote'] = 'on-site'
                    item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnFwUg8FnXNa0YJMwN1Lhp0EloP6gDudyTw2fRNgicRQ&s'

                    yield item
