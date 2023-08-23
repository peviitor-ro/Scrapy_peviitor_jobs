#
#
#
#
# Company Tecknoworks
# https://apply.workable.com/tecknoworks/
#
import scrapy
from scrapy.http import FormRequest
from JobsCrawlerProject.items import JobItem
#
import uuid
#
import json
import requests
import re


class TecknoworksSpiderSpider(scrapy.Spider):
    name = "tecknoworks_spider"
    allowed_domains = ["apply.workable.com"]
    start_urls = ["https://apply.workable.com/tecknoworks/"]

    def start_requests(self):

        session = requests.Session()
        headers_cookie = session.head('https://apply.workable.com/tecknoworks/',
                        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}).headers

        # search data with regex
        wmc = re.search(r'wmc=.*?;', str(headers_cookie['set-cookie'])).group(0)
        cf = re.search(r'__cf', str(headers_cookie['set-cookie'])).group(0)

        # prepare data row and headers for post requests
        formdata = {
                "query": "",
                "location": [],
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
                'referer': 'https://apply.workable.com/tecknoworks/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }

        yield scrapy.Request(
            url='https://apply.workable.com/api/v3/accounts/tecknoworks/jobs',
            method='POST',
            headers=headers,
            body=json.dumps(formdata),
            callback=self.parse
        )

    def parse(self, response):

        for job in response.json()['results']:
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f'https://apply.workable.com/tecknoworks/j/{job["shortcode"]}/'
            item['job_title'] = job['title']
            item['company'] = 'Tecknoworks'
            item['country'] = 'Romania'
            item['city'] = job['location']['city']
            item['logo_company'] = 'https://workablehr.s3.amazonaws.com/uploads/account/logo/543166/logo'

            yield item
