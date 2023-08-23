#
#
#
#
# Company -> AMACH
# Link ----> https://amach.software/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class AmachSpiderSpider(scrapy.Spider):
    name = "amach_spider"
    allowed_domains = ["amach.software"]
    start_urls = ["https://amach.software/careers"]

    def start_requests(self):
        yield scrapy.Request("https://boards.eu.greenhouse.io/embed/job_board?for=amachsoftware")

    def parse(self, response):

        # data here
        for job in response.css('div.opening'):
            city = job.css('span.location::text').get()

            if 'romania' in city.lower():
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('a::attr(href)').get().strip()
                item['job_title'] = job.css('a::text').get().strip()
                item['company'] = 'AMACH'
                item['country'] = 'Romania'
                item['city'] = city.split(',')[0].strip()
                item['logo_company'] = 'https://s101-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/114/210/resized/AMACH-5_Color_Logo_1.png?1675863445'
                #
                yield item
