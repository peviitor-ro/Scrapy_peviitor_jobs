#
#
#
#
# Company -> EWOR
# Link ----> https://join.com/companies/ewor?place%5B0%5D=
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
import uuid


class EworSpiderSpider(CrawlSpider):
    name = "ewor_spider"
    allowed_domains = ["join.com"]
    start_urls = ["https://join.com/companies/ewor?place%5B0%5D=Bra%C8%99ov%2C%20Romania",
                  "https://join.com/companies/ewor?place%5B0%5D=Bucharest%2C%20Romania",
                  "https://join.com/companies/ewor?place%5B0%5D=Cluj-Napoca%2C%20Romania",
                  "https://join.com/companies/ewor?place%5B0%5D=Constan%C8%9Ba%2C%20Romania",
                  "https://join.com/companies/ewor?place%5B0%5D=Craiova%2C%20Romania",
                  ]

    rules = (
            Rule(LinkExtractor(allow=('/companies/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):
        city = response.css('div.sc-gueYoa.sc-1i6aj0b-1.jFHDjD.kPAANs.location')
        if city:
            # parse and send data to pipelines.
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = response.url
            item['job_title'] = response.css('h1.sc-hLseeU.kcOlDA::text').get()
            item['company'] = 'EWOR'
            item['country'] = 'Romania'
            item['city'] = city.css('div.sc-hLseeU.sc-1i6aj0b-2.kJMNsV.eRchHu::text').get().split(',')[0]
            item['logo_company'] = 'https://cdn.join.com/61157a98f4fbb7000885977f/ewor-gmb-h-logo-xl.png'
            #
            yield item
