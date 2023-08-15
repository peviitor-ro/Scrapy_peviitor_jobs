#
#
#
#
# Company -> Globant
# Link ----> https://career.globant.com/
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
import uuid


class GlobantSpiderSpider(CrawlSpider):
    name = "globant_spider"
    allowed_domains = ["career.globant.com"]
    start_urls = ["https://career.globant.com/search/?createNewAlert=false&q=&optionsFacetsDD_department=&optionsFacetsDD_country=RO"]

    rules = (
            Rule(LinkExtractor(allow=('/job/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):

        # get location
        location = response.css('span.jobGeoLocation::text').get()

        # get data
        if 'RO' in location or 'Ro' in location or 'ro' in location:
            #
            # parse data here
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = response.url
            item['job_title'] = response.css('h1::text').get()
            item['company'] = 'Globant'
            item['country'] = 'Romania'
            item['city'] = response.css('span.jobGeoLocation::text').get().split(',')[0]
            item['logo_company'] = 'https://www.globant.com/themes/custom/globant_corp_theme/images/2019/globant-logo-dark.svg'
            yield item
