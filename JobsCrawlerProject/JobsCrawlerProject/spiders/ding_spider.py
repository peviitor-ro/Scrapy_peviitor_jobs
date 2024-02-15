#
#
#
#
# Company -> Ding
# Link ----> https://company.ding.com/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county
#


class DingSpiderSpider(scrapy.Spider):
    name = "ding_spider"
    allowed_domains = ["ding.bamboohr.com"]
    start_urls = ["https://ding.bamboohr.com/careers/list"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for job in response.json().get('result'):

            location = job.get('location').get('city')

            if location.lower() in ['bucharest',]:
                item = JobItem()
                item['job_link'] = 'https://ding.bamboohr.com/careers/' + job['id']
                item['job_title'] = job['jobOpeningName']
                item['company'] = 'Ding'
                item['country'] = 'Romania'
                item['county'] = get_county(location)
                item['city'] = location
                item['remote'] = 'remote' if job.get('isRemote') != None else 'on-site'
                item['logo_company'] = 'https://upload.wikimedia.org/wikipedia/commons/2/23/Ding_logo.png'
                #
                yield item
