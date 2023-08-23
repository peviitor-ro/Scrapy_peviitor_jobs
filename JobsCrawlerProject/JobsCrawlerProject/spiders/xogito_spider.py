#
#
#
#
# Company -> Xogito
# Link ----> https://www.xogito.com/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class XogitoSpiderSpider(scrapy.Spider):
    name = "xogito_spider"
    allowed_domains = ["www.xogito.com"]
    start_urls = ["https://www.xogito.com/careers/"]

    def start_requests(self):
        yield scrapy.Request("https://www.xogito.com/careers/")

    def parse(self, response):

        # extract links from first page
        for job in response.css('div.listing-title'):
            city = response.css('div.listing-title')[0].css('ul.listing-tags').get().lower().split()

            if 'europe' in city:
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('div.listing-title')[0].css('a::attr(href)').get()
                item['job_title'] = job.css('div.listing-title')[0].css('a::text').get().strip()
                item['company'] = 'Xogito'
                item['country'] = 'Romania'
                item['city'] = 'Remote'
                item['logo_company'] = 'https://i0.wp.com/listnet.org/wp-content/uploads/2022/02/xogito-600x450-1.png?fit=600%2C450&ssl=1&w=640'

                yield item
