#
#
#
#
# Company -> Valeo
# Link ----> https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county
#
import json
import re


class ValeoSpiderSpider(scrapy.Spider):
    name = "valeo_spider"
    allowed_domains = ["valeo.wd3.myworkdayjobs.com"]
    start_urls = ["https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122"]

    def start_requests(self):

        formdata = {
            'appliedFacets': {
                'locationCountry': [
                    'f2e609fe92974a55a05fc1cdc2852122',
                ],
            },
            'limit': 20,
            'offset': 0,
            'searchText': '',
        }

        headers = {
            'content-type': 'application/json',
            'origin': 'https://valeo.wd3.myworkdayjobs.com',
            'referer': 'https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }


        yield scrapy.Request(
                url='https://valeo.wd3.myworkdayjobs.com/wday/cxs/valeo/valeo_jobs/jobs',
                method='POST',
                headers=headers,
                body=json.dumps(formdata),
                callback=self.parse
            )

    def parse(self, response):
        print(response.json())

        # parse data from json
        for job in response.json()["jobPostings"]:
            #
            location = job.get('locationsText')
            location_finish = get_county(location=location)
            # 
            item = JobItem()
            item['job_link'] = f'https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs{job.get("externalPath")}?locationCountry=f2e609fe92974a55a05fc1cdc2852122'
            item['job_title'] = job.get('title')
            item['company'] = 'Valeo'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Valeo_Logo.svg/2560px-Valeo_Logo.svg.png'

            yield item
