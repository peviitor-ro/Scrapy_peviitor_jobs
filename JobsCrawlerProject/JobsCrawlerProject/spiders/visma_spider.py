
#
#
#
#
# Company Visma
# https://careers.visma.com/open-positions/?workarea=&country=DH1a5EsqC%2Bnr19a599YPIA%3D%3D&employmenttype=
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid
#
import json


class VismaSpiderSpider(scrapy.Spider):
    name = "visma_spider"
    allowed_domains = ["vismacc.teamtailor.com"]
    start_urls = ["https://careers.visma.com/open-positions/?workarea=&country=DH1a5EsqC%2Bnr19a599YPIA%3D%3D&employmenttype="]

    def start_requests(self):

        formdata = {
                "skip": 0,
                "take": 10,
                "language": "en",
                "workarea": "",
                "country": "DH1a5EsqC+nr19a599YPIA==",
                "city": "",
                "competency": "",
                "subcategory": "",
                "employmenttype": "",
                "sortfield": "PublishDate",
                "sortorder": "asc",
                "text": ""
                }

        headers = {
                'authority': 'careers.visma.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.5',
                'content-type': 'application/json',
                'origin': 'https://careers.visma.com',
                'referer': 'https://careers.visma.com/open-positions/?workarea=&country=DH1a5EsqC%2Bnr19a599YPIA%3D%3D&employmenttype=',
                'user-agent': ' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                }

        yield scrapy.Request(
            url='https://careers.visma.com/api/career/vacancies',
            method='POST',
            headers=headers,
            body=json.dumps(formdata),
            callback=self.parse_links_from_API
        )

    def parse_links_from_API(self, response):
        for job in response.json()["results"]:
            yield scrapy.Request(
                url=job["link"],
                callback=self.parse_job_data
            )

    # parse here jobs data
    def parse_job_data(self, response):
        item = JobItem()
        item['id'] = str(uuid.uuid4())
        item['job_link'] = response.url
        item['job_title'] = response.css('h1.font-company-header::text').get()
        item['company'] = 'Visma'
        item['country'] = 'Romania'
        item['city'] = response.css('dd.w-full::text').getall()[2].strip().split(',')[0].strip()
        item['logo_company'] = 'https://vectorlogoseek.com/wp-content/uploads/2019/02/visma-vector-logo.png'

        yield item
