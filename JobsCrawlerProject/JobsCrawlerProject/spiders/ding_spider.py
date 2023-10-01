#
#
#
#
# Company -> Ding
# Link ----> https://company.ding.com/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class DingSpiderSpider(scrapy.Spider):
    name = "ding_spider"
    allowed_domains = ["ding.bamboohr.com"]
    start_urls = ["https://ding.bamboohr.com/careers/list"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for job in response.json()['result']:

            location = job['location']['city'].strip()

            if location in ['Bucharest']:
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = 'https://ding.bamboohr.com/careers/' + job['id']
                item['job_title'] = job['jobOpeningName']
                item['company'] = 'Ding'
                item['country'] = 'Romania'
                item['city'] = location
                item['logo_company'] = 'https://upload.wikimedia.org/wikipedia/commons/2/23/Ding_logo.png'
                #
                yield item
