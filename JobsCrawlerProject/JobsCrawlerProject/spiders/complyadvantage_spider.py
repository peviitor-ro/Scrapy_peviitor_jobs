#
#
#
#
# Company -> ComplyAdvantage
# Link ----> https://complyadvantage.com/careers/jobs/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class ComplyadvantageSpiderSpider(scrapy.Spider):
    name = "complyadvantage_spider"
    allowed_domains = ["complyadvantage.com"]
    start_urls = ["https://complyadvantage.com/careers/jobs/"]

    def start_requests(self):
        yield scrapy.Request("https://boards.greenhouse.io/embed/job_board?for=complyadvantage&b=https%3A%2F%2Fcomplyadvantage.com%2Fde%2Fstellenangebote%2F")

    def parse(self, response):

        # data here
        for job in response.xpath('//div[contains(@class, "opening")]'):

            # get location
            city = job.xpath('.//span[contains(@class, "location")]/text()').extract_first()
            #
            loc_ready = city.split(',')[0]

            if 'romania' in city.lower():

                location_finish = get_county(location=loc_ready)

                item = JobItem()
                item['job_link'] = job.xpath('.//a/@href').extract_first()
                item['job_title'] = job.xpath('.//a/text()').extract_first()
                item['company'] = 'ComplyAdvantage'
                item['country'] = 'Romania'
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if loc_ready.lower() == location_finish[0].lower()\
                                and True in location_finish and 'bucuresti' != loc_ready.lower()\
                                    else loc_ready
                item['remote'] = 'remote'
                item['logo_company'] = 'https://complyadvantage.com/wp-content/themes/comply/images/logo.svg'
                #
                yield item
