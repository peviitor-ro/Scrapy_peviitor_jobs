#
#
#
#
# Company -> Testronic
# Link ----> https://apply.workable.com/testronic/#jobs
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county
#
import json
#
import requests

class TestronicSpiderSpider(scrapy.Spider):
    name = "testronic_spider"
    allowed_domains = ["apply.workable.com"]
    start_urls = ["https://apply.workable.com/testronic/#jobs"]

    # disable robots.txt for Tesla
    custom_settings = {
            'ROBOTSTXT_OBEY': False
        }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],
                             method='HEAD',
                             callback=self.parse_headers)
        
    def parse_headers(self, response):

        # don't forget split() 
        wmc, cf_bm = [k.decode('utf-8') for\
                      k in response.headers.getlist('Set-Cookie')\
                        if b'wmc' in k or b'cf_bm' in k]

        formdata = {
            'query': '',
            'location': [],
            'department': [],
            'worktype': [],
            'remote': [],
            'workplace': [],
        }

        headers = {
                'authority': 'apply.workable.com',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'cookie': f'{wmc.split()[0]} {cf_bm.split()[0]}',
                'origin': 'https://apply.workable.com',
                'referer': 'https://apply.workable.com/testronic/',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36''
            }

        yield scrapy.Request(
            url='https://apply.workable.com/api/v3/accounts/testronic/jobs',
            method='POST',
            headers=headers,
            body=json.dumps(formdata),
            callback=self.parse
        )

    def parse(self, response):
        print(response)

    #     # parse jobs here
    #     for job in response.json()["results"]:
    #         item = JobItem()
    #         item['id'] = str(uuid.uuid4())
    #         item['job_link'] = f'https://apply.workable.com/testronic/j/{job["shortcode"]}'
    #         item['job_title'] = job['title']
    #         item['company'] = 'Testronic'
    #         item['country'] = 'Romania'
    #         item['city'] = job['location']['city']
    #         item['logo_company'] = 'https://workablehr.s3.amazonaws.com/uploads/account/logo/585016/logo'

    #         yield item