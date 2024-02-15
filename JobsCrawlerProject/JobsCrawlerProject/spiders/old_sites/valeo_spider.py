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
import uuid
import json
import re


class ValeoSpiderSpider(scrapy.Spider):
    name = "valeo_spider"
    allowed_domains = ["valeo.wd3.myworkdayjobs.com"]
    start_urls = ["https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122"]

    def start_requests(self):
        yield scrapy.Request(url='https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122',
                             callback=self.parse_headers, method='HEAD')

    def parse_headers(self, response):
        self.headers = response.headers

        wd_browser_id = re.search(r'wd-browser-id=([\w-]+);', str(self.headers)).group(0)
        calypso_csrf = re.search(r'CALYPSO_CSRF_TOKEN=([\w-]+);', str(self.headers)).group(0)
        play_session_id = re.search(r'PLAY_SESSION=([^;]+);', str(self.headers)).group(0)
        ts_id = re.search(r'TS[^;]+;', str(self.headers)).group(0)

        # start post requests here
        formdata = {"appliedFacets": {
                "locationCountry": ["f2e609fe92974a55a05fc1cdc2852122"]
            },
            "limit": 20,
            "offset": 0,
            "searchText": ""
                 }

        headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en-US',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Cookie': f'{play_session_id} timezoneOffset=-180; {ts_id} {wd_browser_id} {calypso_csrf[:-1]}',
                'Origin': 'https://valeo.wd3.myworkdayjobs.com',
                'Referer': 'https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'X-CALYPSO-CSRF-TOKEN': f'{calypso_csrf.split("=")[:-1]}',
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
            }

        yield scrapy.Request(
                url='https://valeo.wd3.myworkdayjobs.com/wday/cxs/valeo/valeo_jobs/jobs',
                method='POST',
                headers=headers,
                body=json.dumps(formdata),
                callback=self.parse
            )

    def parse(self, response):

        # parse data from json
        for job in response.json()["jobPostings"]:
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f'https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs{job["externalPath"]}?locationCountry=f2e609fe92974a55a05fc1cdc2852122'
            item['job_title'] = job["title"]
            item['company'] = 'Valeo'
            item['country'] = 'Romania'
            item['city'] = job["locationsText"]
            item['logo_company'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Valeo_Logo.svg/2560px-Valeo_Logo.svg.png'

            yield item
