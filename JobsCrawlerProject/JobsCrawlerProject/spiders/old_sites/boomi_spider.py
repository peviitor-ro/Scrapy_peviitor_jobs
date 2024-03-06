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


class BoomiSpiderSpider(scrapy.Spider):
    name = "boomi_spider"
    allowed_domains = ["boards-api.greenhouse.io"]
    start_urls = ["https://boards-api.greenhouse.io/v1/boards/boomilp/departments"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for job in response.json().get('departments'):
            for level_2_job in job.get('jobs'):

                # find job location and verify if it available
                job_location = level_2_job.get('location').get('name')
                if job_location and "romania" == job_location.lower():

                    print(job_location)
                    #
                    item = JobItem()
                    item['job_link'] = level_2_job['absolute_url']
                    item['job_title'] = level_2_job['title']
                    item['company'] = 'Boomi'
                    item['country'] = 'Romania'
                    item['county'] = ''
                    item['city'] = level_2_job['metadata'][1]['value'].split()[0]
                    item['remote'] = ''
                    item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWghf5zFKDsY-zVbX4Jd-H5GZfAqEdBpn-FR1DIquz2fn7nCiBeKrFYykE1qb9fNvNxkY'
                    #
                    yield item
