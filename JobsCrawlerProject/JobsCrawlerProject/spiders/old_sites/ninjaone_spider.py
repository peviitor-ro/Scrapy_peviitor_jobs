#
#
#
#
# Company -> NinjaOne
# Link ----> https://www.ninjaone.com/careers/#open-positions
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class NinjaoneSpiderSpider(scrapy.Spider):
    name = "ninjaone_spider"
    allowed_domains = ["www.ninjaone.com"]
    start_urls = ["https://www.ninjaone.com/careers/#open-positions"]

    def start_requests(self):
        yield scrapy.Request("https://ninjarmm-llc.hirehive.com/api/v1/jobs?take=500&skip=0&countryCode=&category=&source=CareerSite")

    def parse(self, response):

        for job in response.json()["jobs"]:
            country = job["country"]["name"]

            if country == "Romania":
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job["hostedUrl"]
                item['job_title'] = job["title"]
                item['company'] = 'NinjaOne'
                item['country'] = country
                item['city'] = job["location"]
                item['logo_company'] = 'https://www.logo-designer.co/storage/2022/08/2021-it-firm-ninjaone-new-logo-design.png'
                #
                yield item
