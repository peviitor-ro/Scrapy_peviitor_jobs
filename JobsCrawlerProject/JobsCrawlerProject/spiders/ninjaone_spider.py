#
#
#
#
# Company -> NinjaOne
# Link ----> https://www.ninjaone.com/careers/#open-positions
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class NinjaoneSpiderSpider(scrapy.Spider):
    name = "ninjaone_spider"
    allowed_domains = ["www.ninjaone.com"]
    start_urls = ["https://www.ninjaone.com/careers/#open-positions"]

    def start_requests(self):
        yield scrapy.Request("https://ninjarmm-llc.hirehive.com/api/v1/jobs?take=500&skip=0&countryCode=&category=&source=CareerSite")

    def parse(self, response):

        for job in response.json()["jobs"]:
            country = job["country"]["name"]

            if country == "Romania":

                if (location := job.get('location').strip().lower()) == 'bucharest':
                    location = 'Bucuresti'
                location_finish = get_county(location=location)

                item = JobItem()
                item['job_link'] = job.get("hostedUrl")
                item['job_title'] = job.get("title")
                item['company'] = 'NinjaOne'
                item['country'] = country
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location
                item['remote'] = 'remote'
                item['logo_company'] = 'https://www.logo-designer.co/storage/2022/08/2021-it-firm-ninjaone-new-logo-design.png'
                #
                yield item
