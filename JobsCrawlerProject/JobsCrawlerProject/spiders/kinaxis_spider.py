#
#
#
#
# Company -> Kinaxis
# Link ----> https://boards.greenhouse.io/kinaxis
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import counties, get_county


class KinaxisSpiderSpider(scrapy.Spider):
    name = "kinaxis_spider"
    allowed_domains = ["boards.greenhouse.io"]
    start_urls = ["https://boards.greenhouse.io/kinaxis"]

    def start_requests(self):
        yield scrapy.Request("https://boards.greenhouse.io/kinaxis")

    def parse(self, response):

        # data here
        for job in response.xpath('//div[@class="opening"]'):

            # get location
            city = job.xpath('.//span[@class="location"]/text()').extract()[0].lower().split(',')

            # check for Romania location
            if 'romania' in [element.strip() for element in city]:

                # get location from county
                location = ''
                for city_and_counties in counties:
                    for key, value in city_and_counties.items():
                        if key == city[0].title():
                            for new_city in value:
                                if city[0].title().strip() in new_city:
                                    location = new_city
                if location == '':
                    location = city[0].title()

                item = JobItem()
                item['job_link'] = 'https://boards.greenhouse.io' + job.xpath('.//a/@href').extract_first()
                item['job_title'] = job.xpath('.//a/text()').extract_first()
                item['company'] = 'Kinaxis'
                item['country'] = 'Romania'
                item['county'] = get_county(location)
                item['city'] = location
                item['remote'] = 'remote'
                item['logo_company'] = 'https://www.kinaxis.com/themes/custom/kinaxis/logo.png'
                #
                yield item
