#
#
#
#
# Company -> Upscale
# Link ----> https://upscale.ai/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class UpscaleSpiderSpider(scrapy.Spider):
    name = "upscale_spider"
    allowed_domains = ["devwordpress.upscale.ai"]
    start_urls = ["https://devwordpress.upscale.ai/wp-json/wp/v2/career?&meta=true&order=desc&order_by=date&status=publish"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        #
        for job in response.json():
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f"https://upscale.ai/careers/{job['link'].split('/')[-2]}"
            item['job_title'] = job['title']['rendered']
            item['company'] = 'Upscale'
            item['country'] = 'Romania'
            item['city'] = 'Remote'
            item['logo_company'] = 'https://upscale.ai/images/common/svg/upscaleLogo.svg'
            #
            yield item
