#
#
#
#
# Company -> Kadra
# Link ----> https://kadragroup.com/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county, remove_diacritics, counties
#
import re


class KadraSpiderSpider(scrapy.Spider):
    name = "kadra_spider"
    allowed_domains = ["kadragroup.com"]
    start_urls = ["https://kadragroup.com/careers/"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        # parse job data!
        for job in response.xpath('//div[contains(@class, "single_toggle")]'):

            # algorithm for location
            title_location = job.xpath('.//p/text()')[0].extract()
                        
            # search by location name
            location = None
            for county_and_city in counties:
                for key, value in county_and_city.items():

                    # append county to value: list! with locations
                    value.append(key)
                    for city in value:
                        city = remove_diacritics(city)
                        location_remove_diacritics = remove_diacritics(title_location)

                        # specific city from found_county - counties
                        if re.search(r'\b{}\b'.format(re.escape(city.split()[-1].lower())), location_remove_diacritics.lower()):
                            location = city

            location_finish = get_county(location=location)


            item = JobItem()
            item['job_link'] = 'https://kadragroup.com/careers/' \
                                        + job.xpath('.//p/@data-fake-id')[0].extract()
            item['job_title'] = title_location
            item['company'] = 'Kadra'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                and True in location_finish and 'bucuresti' != location.lower()\
                                    else location
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://kadra.ro/wp-content/uploads/2018/11/logo-Kadra-wide-500.png'
            #
            yield item
