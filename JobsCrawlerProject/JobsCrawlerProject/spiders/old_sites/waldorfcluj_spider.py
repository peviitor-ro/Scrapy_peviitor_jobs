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

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        ul_li = response.css('ul.has-medium-font-size')
        if ul_li:
            for job in ul_li[0].css('li'):
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('a::attr(href)').get()
                item['job_title'] = job.css('a::text').get().capitalize()[:-1]
                item['company'] = 'WaldorfCluj'
                item['country'] = 'Romania'
                item['city'] = 'Cluj'
                item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnFwUg8FnXNa0YJMwN1Lhp0EloP6gDudyTw2fRNgicRQ&s'

                yield item
