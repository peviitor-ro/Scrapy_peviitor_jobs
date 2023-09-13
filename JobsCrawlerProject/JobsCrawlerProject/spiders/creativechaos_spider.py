#
#
#
#
# Company -> CreativeChaos
# Link -----> https://apply.workable.com/creativechaos/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid
#
import json
import requests
import re


class CreativechaosSpiderSpider(scrapy.Spider):
    name = "creativechaos_spider"
    allowed_domains = ["apply.workable.com"]
    start_urls = ["https://apply.workable.com/creativechaos/"]

    def start_requests(self):

        session = requests.Session()
        headers_cookie = session.head('https://apply.workable.com/creativechaos/',
                        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}).headers

        # search data with regex
        wmc = re.search(r'wmc=.*?;', str(headers_cookie['set-cookie'])).group(0)
        cf = re.search(r'__cf', str(headers_cookie['set-cookie'])).group(0)

        # prepare data row and headers for post request
        formdata = {
            "query": "",
            "location": [{"country": "Romania", "countryCode": "RO"}],
            "department": [],
            "worktype": [],
            "remote": []
            }

        headers_cookie = {
            'authority': 'apply.workable.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en',
            'content-type': 'application/json',
            'cookie': f'{wmc} {cf}',
            'origin': 'https://apply.workable.com',
            'referer': 'https://apply.workable.com/creativechaos/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }

        yield scrapy.Request(
            url='https://apply.workable.com/api/v3/accounts/creativechaos/jobs',
            method='POST',
            headers=headers_cookie,
            body=json.dumps(formdata),
            callback=self.parse
        )

    def parse(self, response):

        # parse jobs data!
        for job in response.json()["results"]:
            if ((location := job['location']['city']) == ''):
                location = 'Remote'
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f'https://apply.workable.com/creativechaos/j/{job["shortcode"]}/'
            item['job_title'] = job['title']
            item['company'] = 'CreativeChaos'
            item['country'] = 'Romania'
            item['city'] = location
            item['logo_company'] = 'https://workablehr.s3.amazonaws.com/uploads/account/logo/496284/logo'

            yield item
