#
#
#
#
# Company -> Roweb
# Link ----> https://www.roweb.ro/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class RowebSpiderSpider(scrapy.Spider):
    name = "roweb_spider"
    allowed_domains = ["www.roweb.ro"]
    start_urls = ["https://www.roweb.ro/careers"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for job in response.css('div.cards-wrapper > div.card'):
            link = job.css('a.sg-jobs-card-button::attr(href)').get()

            if link:
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = 'https://www.roweb.ro/' + link
                item['job_title'] = job.css('div.content-wrapper > h3::text').get()
                item['company'] = 'Roweb'
                item['country'] = 'Romania'
                item['city'] = job.css('div.content-wrapper > p::text').get().split()[-1]
                item['logo_company'] = 'https://interfoane.ro/wp-content/uploads/2016/11/roweb.jpg'
                #
                yield item
