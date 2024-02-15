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
from JobsCrawlerProject.found_county import get_county


class FlashnetSpiderSpider(scrapy.Spider):
    name = "flashnet_spider"
    allowed_domains = ["www.flashnet.ro"]
    start_urls = ["https://www.flashnet.ro/our-people/#!/jobs"]

    def start_requests(self):
        yield scrapy.Request("https://www.flashnet.ro/our-people/#!/jobs")

    def parse(self, response):

        # parse data from this site!
        for link in response.xpath('//article[contains(@class, "post") and contains(@class, "project-odd")]//a[@class="post-thumbnail-rollover"]/@href').extract():
            yield scrapy.Request(link, callback=self.parse_job_data)

    def parse_job_data(self, response):

        item = JobItem()
        item['job_link'] = response.url
        item['job_title'] = response.xpath('//h2[@class="vc_custom_heading"]/text()').extract_first()
        item['company'] = 'Flashnet'
        item['country'] = 'Romania'
        item['county'] = 'Brasov'
        item['city'] = 'Brasov'
        item['remote'] = 'on-site'
        item['logo_company'] = 'https://storage0.dms.mpinteractiv.ro/media/401/781/10686/21666533/3/flashnet-logo.jpg'
        #
        yield item
