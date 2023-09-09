#
#
#
#
# Company -> Kadra
# Link ----> https://kadragroup.com/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class KadraSpiderSpider(scrapy.Spider):
    name = "kadra_spider"
    allowed_domains = ["kadragroup.com"]
    start_urls = ["https://kadragroup.com/careers/"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        # parse job data!
        for job in response.css('div.single_toggle'):
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = 'https://kadragroup.com/careers/#' \
                                        + job.css('p[aria-controls]::attr(aria-controls)').extract_first()
            item['job_title'] = job.css('p.toggler::text').get()
            item['company'] = 'Kadra'
            item['country'] = 'Romania'
            item['city'] = 'Romania'
            item['logo_company'] = 'https://kadra.ro/wp-content/uploads/2018/11/logo-Kadra-wide-500.png'
            #
            yield item
