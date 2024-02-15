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

            # get all cities
            cities_from_titles = set()
            counties_from_titles = set()
            for county_and_city in counties:
                for key, value in county_and_city.items():
                    for city in value:
                        city = remove_diacritics(city)
                        loc_diac = remove_diacritics(title_location)

                        # if in loc_diac not diacritics
                        if re.search(r'\b{}\b'.format(re.escape(city.split()[-1].lower())), loc_diac.lower()):
                            cities_from_titles.add(city)
                            counties_from_titles.add(key)

                # on one job, we have only county - Cluj. I made a Search by key in values
                else:
                    if len(cities_from_titles) == 0:
                        for keys, values in county_and_city.items():
                            if re.search(r'\b{}\b'.format(re.escape(keys.split()[-1].lower())), remove_diacritics(title_location).lower()):
                                for new_c in values:
                                    if keys in new_c:
                                        cities_from_titles.add(new_c)
                                        counties_from_titles.add(keys)
                        


            item = JobItem()
            item['job_link'] = 'https://kadragroup.com/careers/' \
                                        + job.xpath('.//p/@data-fake-id')[0].extract()
            item['job_title'] = title_location
            item['company'] = 'Kadra'
            item['country'] = 'Romania'
            item['county'] = list(counties_from_titles)[0] if 0 < len(counties_from_titles) < 2 else list(counties_from_titles)
            item['city'] = list(cities_from_titles)[0] if 0 < len(cities_from_titles) < 2 else list(cities_from_titles)
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://kadra.ro/wp-content/uploads/2018/11/logo-Kadra-wide-500.png'
            #
            yield item
