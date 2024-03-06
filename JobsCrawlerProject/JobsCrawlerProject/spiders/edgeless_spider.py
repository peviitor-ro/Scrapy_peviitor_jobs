#
#
#
#
# Company -> EdgeLess
# Link ----> http://www.edgeless.ro/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class EdgelessSpiderSpider(scrapy.Spider):
    name = "edgeless_spider"
    allowed_domains = ["www.edgeless.ro"]
    start_urls = ["http://www.edgeless.ro/careers/#jobs"]

    def start_requests(self):
        yield scrapy.Request("http://www.edgeless.ro/careers/")

    def parse(self, response):

        # parse links to jobs here
        for job in response.xpath('//div[@class="elementor-flip-box__layer__inner"]'):

            if (link := job.xpath('.//a[contains(@class, "elementor-flip-box__button elementor-button")]/@href').extract_first()):
                yield scrapy.Request(url=link, callback=self.parse_job_details)

    def parse_job_details(self, response):

        # parse location because it needed in tow diferent places
        if (location := response.xpath('//li//span/text()').extract()[-2].lower()) == 'bucharest':
            location = 'Bucuresti'

        location_finish = get_county(location=location)

        # parse data and send it to pipelines.py
        item = JobItem()
        item['job_link'] = response.url
        item['job_title'] = response.xpath('//h1[contains(@class, "elementor-heading-title")]/text()').extract()[-1]
        item['company'] = 'EdgeLess'
        item['country'] = 'Romania'
        item['county'] = location_finish[0] if True in location_finish else None
        item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location
        item['remote'] = 'on-site'
        item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXKx4pqVnhEvKxETB_rWvem5yJpmEv_jkNaM2eGHsK0w&s'
        #
        yield item
