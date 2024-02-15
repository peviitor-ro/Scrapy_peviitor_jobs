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
from JobsCrawlerProject.found_county import get_county


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
        location = response.xpath('//div[@class="ng-star-inserted"]//text()').extract_first().strip()
        if (correct_location := location.split(',')[0]).lower() == 'bucharest':
            correct_location = "Bucuresti"

        # get data
        if 'romania' in location.lower():
            #
            item = JobItem()
            item['job_link'] = response.url
            item['job_title'] = response.xpath('//h1[contains(@class, "title-label")]/text()').extract_first().strip()
            item['company'] = 'GridDynamics'
            item['country'] = 'Romania'
            item['county'] = get_county(correct_location.title())
            item['city'] = correct_location.title()
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://itkonekt.com/media/2019/02/2019-02-26.png'
            #
            yield item
