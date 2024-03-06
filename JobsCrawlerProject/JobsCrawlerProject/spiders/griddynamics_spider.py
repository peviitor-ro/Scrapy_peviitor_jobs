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
from JobsCrawlerProject.found_county import get_county


class GriddynamicsSpiderSpider(CrawlSpider):
    '''
        Spider for Gryddynamic Company
    '''

    name = "griddynamics_spider"
    allowed_domains = ["careers.griddynamics.com"]
    start_urls = ["https://careers.griddynamics.com/discover-openings?location=Bucharest,%20Romania"]

    rules = (
            Rule(LinkExtractor(allow=('/discover-openings/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):
        '''
        ... parse metod for rules. Extract all data from griddynamics company
        '''

        # get location
        location = response.xpath('//div[@class="ng-star-inserted"]//text()').extract_first().strip()
        if (correct_location := location.split(',')[0]).lower() == 'bucharest':
            correct_location = "Bucuresti"

        # get data
        if 'romania' in location.lower():

            location_finish = get_county(location=correct_location)
            #
            item = JobItem()
            item['job_link'] = response.url
            item['job_title'] = response.xpath('//h1[contains(@class, "title-label")]/text()').extract_first().strip()
            item['company'] = 'GridDynamics'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if correct_location.lower() == location_finish[0].lower()\
                                and True in location_finish and 'bucuresti' != correct_location.lower()\
                                    else correct_location.title()
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://itkonekt.com/media/2019/02/2019-02-26.png'
            #
            yield item
