#
#
#
#
# Company -> Testronic
# Link ----> https://apply.workable.com/testronic/#jobs
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid
import json
import re
#
import requests


class TestronicSpiderSpider(scrapy.Spider):
    name = "testronic_spider"
    allowed_domains = ["apply.workable.com"]
    start_urls = ["https://apply.workable.com/testronic/#jobs"]

    def start_requests(self):

        # extract fresh cookies every time
        _cookies = requests.head('https://apply.workable.com/testronic', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X; ru-UA) AppleWebKit/537.36 (KHTML, like Gecko) Version/11.2.6 Mobile/15D100 Safari/537.36 Puffin/5.2.2IP'}).headers

        # search data with regex
        wmc = re.search(r'wmc=.*?;', str(_cookies['set-cookie'])).group(0)
        cf = re.search(r'__cf', str(_cookies['set-cookie'])).group(0)

        formdata = {
                 "query": "",
                 "location": [
                     {
                         "country": "Romania",
                         "region": "Bucharest",
                         "city": "Bucharest",
                         "countryCode": "RO"
                     }
                 ],
                 "department": [],
                 "worktype": [],
                 "remote": []
             }

        headers = {
                'authority': 'apply.workable.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en',
                'content-type': 'application/json',
                'cookie': f'{wmc} {cf}',
                'origin': 'https://apply.workable.com',
                'referer': 'https://apply.workable.com/testronic/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }

        yield scrapy.Request(
            url='https://apply.workable.com/api/v3/accounts/testronic/jobs',
            method='POST',
            headers=headers,
            body=json.dumps(formdata),
            callback=self.parse
        )

    def parse(self, response):

        # parse jobs here
        for job in response.json()["results"]:
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f'https://apply.workable.com/testronic/j/{job["shortcode"]}'
            item['job_title'] = job['title']
            item['company'] = 'Testronic'
            item['country'] = 'Romania'
            item['city'] = job['location']['city']
            item['logo_company'] = 'https://workablehr.s3.amazonaws.com/uploads/account/logo/585016/logo'

            yield item
