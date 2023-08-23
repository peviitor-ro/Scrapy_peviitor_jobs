#
#
#
#
# Company -> Flashnet
# Link ----> https://www.flashnet.ro/our-people/#!/jobs
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class FlashnetSpiderSpider(scrapy.Spider):
    name = "flashnet_spider"
    allowed_domains = ["www.flashnet.ro"]
    start_urls = ["https://www.flashnet.ro/our-people/#!/jobs"]

    def start_requests(self):
        yield scrapy.Request("https://www.flashnet.ro/our-people/#!/jobs")

    def parse(self, response):

        # parse data from this site!
        for job in response.css('div.post-entry-content'):

            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = job.css('div.post-entry-content a::attr(href)').get()
            item['job_title'] = job.css('div.post-entry-content a::text').get()
            item['company'] = 'Flashnet'
            item['country'] = 'Romania'
            item['city'] = job.css('div.post-entry-content a::text').get().split(',')[-1].strip()
            item['logo_company'] = 'https://storage0.dms.mpinteractiv.ro/media/401/781/10686/21666533/3/flashnet-logo.jpg'
            #
            yield item
