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
import uuid


class ComplyadvantageSpiderSpider(scrapy.Spider):
    name = "complyadvantage_spider"
    allowed_domains = ["complyadvantage.com"]
    start_urls = ["https://complyadvantage.com/careers/jobs/"]

    def start_requests(self):
        yield scrapy.Request("https://boards.greenhouse.io/embed/job_board?for=complyadvantage&b=https%3A%2F%2Fcomplyadvantage.com%2Fde%2Fstellenangebote%2F")

    def parse(self, response):

        # data here
        for job in response.css('div.opening'):
            city = job.css('span.location::text').get().strip()

            if 'romania' in city.lower():
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('a::attr(href)').get().strip()
                item['job_title'] = job.css('a::text').get().strip()
                item['company'] = 'ComplyAdvantage'
                item['country'] = 'Romania'
                item['city'] = city.split(',')[0]
                item['logo_company'] = 'https://complyadvantage.com/wp-content/themes/comply/images/logo.svg'
                #
                yield item
