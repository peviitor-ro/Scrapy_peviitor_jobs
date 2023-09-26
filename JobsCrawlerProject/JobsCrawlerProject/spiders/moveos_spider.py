#
#
#
#
# Company -> Moveos
# Link ----> https://www.hr.moveos.ro/en/jobs/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class MoveosSpiderSpider(scrapy.Spider):
    name = "moveos_spider"
    allowed_domains = ["www.hr.moveos.ro"]
    start_urls = ["https://www.hr.moveos.ro/en/jobs/"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        # parse jobs here
        for job in response.css('div.fusion-portfolio-content'):
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = job.css('a::attr(href)').get()
            item['job_title'] = job.css('a::text').get()
            item['company'] = 'Moveos'
            item['country'] = 'Romania'
            item['city'] = 'Romania'
            item['logo_company'] = 'https://www.hr.moveos.ro/wp-content/uploads/2021/05/moveos.logo_.jpg'
            #
            yield item
