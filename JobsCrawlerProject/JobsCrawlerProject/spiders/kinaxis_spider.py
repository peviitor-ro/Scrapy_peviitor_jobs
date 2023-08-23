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
import uuid


class KinaxisSpiderSpider(scrapy.Spider):
    name = "kinaxis_spider"
    allowed_domains = ["boards.greenhouse.io"]
    start_urls = ["https://boards.greenhouse.io/kinaxis"]

    def start_requests(self):
        yield scrapy.Request("https://boards.greenhouse.io/kinaxis")

    def parse(self, response):

        # data here
        for job in response.css('div.opening'):

            # get location
            city = job.css('span.location::text').get().strip()

            # check for Romania location
            if 'romania' in city.lower():
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = 'https://boards.greenhouse.io' + job.css('a::attr(href)').get().strip()
                item['job_title'] = job.css('a::text').get().strip()
                item['company'] = 'Kinaxis'
                item['country'] = 'Romania'
                item['city'] = city.split(',')[0]
                item['logo_company'] = 'https://www.kinaxis.com/themes/custom/kinaxis/logo.png'
                #
                yield item
