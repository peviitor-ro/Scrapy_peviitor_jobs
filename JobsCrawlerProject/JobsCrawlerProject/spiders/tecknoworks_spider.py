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
import json


class TecknoworksSpiderSpider(scrapy.Spider):
    name = "tecknoworks_spider"
    allowed_domains = ["apply.workable.com"]
    start_urls = ["https://apply.workable.com/tecknoworks/"]

    def start_requests(self):

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
                'content-type': 'application/json',
                'origin': 'https://apply.workable.com',
                'referer': 'https://apply.workable.com/tecknoworks/',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
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
            item['job_link'] = f'https://apply.workable.com/tecknoworks/j/{job.get("shortcode")}/'
            item['job_title'] = job.get('title')
            item['company'] = 'Tecknoworks'
            item['country'] = 'Romania'
            item['county'] = job.get('location').get('region').split()[0]
            item['city'] = job.get('location').get('city')
            item['remote'] = job.get('workplace')
            item['logo_company'] = 'https://workablehr.s3.amazonaws.com/uploads/account/logo/543166/logo'

            yield item
