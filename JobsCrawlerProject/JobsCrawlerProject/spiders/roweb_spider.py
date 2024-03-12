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
        for job in response.xpath('//div[@class="content-wrapper"]'):

            if (link := job.xpath('.//a[@class="sg-jobs-card-button"]/@href').extract_first()):

                location = job.xpath('.//p/text()').extract()
                if 'remote' in location[0].lower() and 'or' in location[0].lower():
                    location = location[0].split('or')[0].strip().split(',')

                item = JobItem()
                item['job_link'] = 'https://www.roweb.ro/' + link
                item['job_title'] = job.xpath('.//h3/text()').extract_first()
                item['company'] = 'Roweb'
                item['country'] = 'Romania'
                item['country'] = ''
                item['city'] = location
                item['remote'] = 'on-site'
                item['logo_company'] = 'https://interfoane.ro/wp-content/uploads/2016/11/roweb.jpg'
                #
                yield item
