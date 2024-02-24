#
#
#
#
# Company -> NeobyteSolutions
# Link ----> https://www.neobytesolutions.com/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class NeobytesolutionsSpiderSpider(scrapy.Spider):
    name = "neobytesolutions_spider"
    allowed_domains = ["www.neobytesolutions.com"]
    start_urls = ["https://www.neobytesolutions.com/careers/"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        # parse jobs
        for job in response.xpath('//div[contains(@class, "panel") and contains(@class, "panel-default")]'):
            item = JobItem()
            item['job_link'] = job.xpath('.//div[@class="panel-body"]//a/@href').extract_first()
            item['job_title'] = job.xpath('.//h4[@class="panel-title"]/text()').extract_first()
            item['company'] = 'NeobyteSolutions'
            item['country'] = 'Romania'
            item['county'] = 'Bihor'
            item['city'] = 'Oradea'
            item['remote'] = 'hybrid'
            item['logo_company'] = 'https://www.neobytesolutions.com/wp-content/uploads/2022/04/logo_Neobyte_solutions-Bold.webp'
            
            yield item
