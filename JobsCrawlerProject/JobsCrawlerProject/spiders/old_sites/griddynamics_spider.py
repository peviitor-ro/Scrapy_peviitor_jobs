#
#
#
#
# Company -> GridDynamics
# Link ----> https://careers.griddynamics.com/discover-openings?location=Bucharest,%20Romania
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
import uuid


class GriddynamicsSpiderSpider(CrawlSpider):
    name = "griddynamics_spider"
    allowed_domains = ["careers.griddynamics.com"]
    start_urls = ["https://careers.griddynamics.com/discover-openings?location=Bucharest,%20Romania"]

    rules = (
            Rule(LinkExtractor(allow=('/discover-openings/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):

        # get location
        location = response.css('div.gd-typography-body.underline-text.ng-star-inserted > div.ng-star-inserted::text').get().strip()

        # get data
        if 'romania' in location.lower():
            #
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = response.url
            item['job_title'] = response.css('h1.gd-typography-h2.title-label::text').get().strip()
            item['company'] = 'GridDynamics'
            item['country'] = 'Romania'
            item['city'] = location.split(',')[0]
            item['logo_company'] = 'https://itkonekt.com/media/2019/02/2019-02-26.png'
            #
            yield item
