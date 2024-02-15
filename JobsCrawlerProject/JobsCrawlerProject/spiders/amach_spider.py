#
#
#
#
import scrapy
from JobsCrawlerProject.items import JobItem

# personal scripts
from JobsCrawlerProject.get_job_type import get_job_type
from JobsCrawlerProject.found_county import get_county


class AmachSpiderSpider(scrapy.Spider):
    name = "amach_spider"
    allowed_domains = ["amach.software", "boards.eu.greenhouse.io"]
    start_urls = ["https://boards.eu.greenhouse.io/embed/job_board/?for=amach"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        # data here
        for job in response.xpath('//div[@class="opening"]'):
            city_tag = job.xpath('.//span[@class="location"]/text()').get()
            
            # check city
            if 'romania' in city_tag.lower():
                new_city = city_tag.split(',')[0].strip()
                if new_city.lower() == 'bucharest':
                    new_city = 'Bucuresti'
                #
                item =JobItem()
                item['job_link'] = job.xpath('.//a/@href').get()
                item['job_title'] = job.xpath('.//a/text()').get()
                item['company'] = 'AMACH'
                item['country'] = 'Romania'
                item['county'] = get_county(new_city)
                item['city'] = new_city
                item['remote'] = 'on-site'
                item['logo_company'] = 'https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/114/210/resized/AMACH-5_Color_Logo_1.png?1675863445'
                #
                yield item