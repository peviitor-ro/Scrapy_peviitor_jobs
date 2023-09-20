#
#
#
#
#
#
#
#
#
# Company -> Boomi
# Link ----> https://boomi.com/company/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class BoomiSpiderSpider(scrapy.Spider):
    name = "boomi_spider"
    allowed_domains = ["boards-api.greenhouse.io"]
    start_urls = ["https://boards-api.greenhouse.io/v1/boards/boomilp/departments"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        # parse jobs!
        for job in response.json()['departments']:
            for level_2_job in job['jobs']:
                if 'romania' == level_2_job['location']['name'].lower():
                    #
                    item = JobItem()
                    item['id'] = str(uuid.uuid4())
                    item['job_link'] = level_2_job['absolute_url']
                    item['job_title'] = level_2_job['title']
                    item['company'] = 'Boomi'
                    item['country'] = 'Romania'
                    item['city'] = level_2_job['metadata'][1]['value'].split()[0]
                    item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWghf5zFKDsY-zVbX4Jd-H5GZfAqEdBpn-FR1DIquz2fn7nCiBeKrFYykE1qb9fNvNxkY'
                    #
                    yield item
