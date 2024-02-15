#
#
#
#
# Company -> Signicat
# Link ----> https://www.signicat.com/about/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class SignicatSpiderSpider(scrapy.Spider):
    name = "signicat_spider"
    allowed_domains = ["www.signicat.com"]
    start_urls = ["https://signicat.teamtailor.com/jobs"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        for job in response.css('li.w-full'):
            location = job.css('div.mt-1.text-md').get()

            if location and 'romania' in location.lower():
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('a::attr(href)').get()
                item['job_title'] = job.css('span.text-block-base-link::text').get()
                item['company'] = 'Signicat'
                item['country'] = 'Romania'
                item['city'] = 'Bucuresti'
                item['logo_company'] = 'https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/cbd19f90-5af8-4896-b889-d91ab4f32b07/original.png'

                yield item
