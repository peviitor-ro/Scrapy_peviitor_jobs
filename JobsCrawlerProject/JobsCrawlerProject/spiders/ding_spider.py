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

    def parse(self, response):
        for job in response.json().get('result'):

            location = job.get('location').get('city')

            if location != None:
                if location.lower() in ['bucharest',]:
                    location_finish = get_county(location=location)
                    item = JobItem()
                    item['job_link'] = 'https://ding.bamboohr.com/careers/' + job['id']
                    item['job_title'] = job['jobOpeningName']
                    item['company'] = 'Ding'
                    item['country'] = 'Romania'
                    item['county'] = location_finish[0] if True in location_finish else None
                    item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                        and True in location_finish and 'bucuresti' != location.lower()\
                                            else location
                    item['remote'] = 'remote' if job.get('isRemote') != None else 'on-site'
                    item['logo_company'] = 'https://upload.wikimedia.org/wikipedia/commons/2/23/Ding_logo.png'
                    #
                    yield item
