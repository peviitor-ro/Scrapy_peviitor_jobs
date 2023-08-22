#
#
#
#
# Company -> VIAVI
# Link ----> https://viavisolutions.wd1.myworkdayjobs.com/careers?locations=992601fe562601082aa1272846780000
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from bs4 import BeautifulSoup
#
import uuid
import json
#
import re


class ViaviSpiderSpider(scrapy.Spider):
    name = "viavi_spider"
    allowed_domains = ["viavisolutions.wd1.myworkdayjobs.com"]
    start_urls = ["https://viavisolutions.wd1.myworkdayjobs.com/careers?locations=992601fe562601082aa1272846780000"]

    custom_settings = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    def start_requests(self):
        yield scrapy.Request(url='https://valeo.wd3.myworkdayjobs.com/en-US/valeo_jobs?locationCountry=f2e609fe92974a55a05fc1cdc2852122',
                             callback=self.parse_headers, method='HEAD')

    def parse_headers(self, response):
        self.headers = response.headers

        wd_browser_id = re.search(r'wd-browser-id=([\w-]+);', str(self.headers)).group(0)
        calypso_csrf = re.search(r'CALYPSO_CSRF_TOKEN=([\w-]+);', str(self.headers)).group(0)
        play_session_id = re.search(r'PLAY_SESSION=([^;]+);', str(self.headers)).group(0)
        ts_id = re.search(r'TS[^;]+;', str(self.headers)).group(0)

        formdata = {
                "appliedFacets": {
                    "locations": ["992601fe562601082aa1272846780000"]
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
                'Cookie': f'{play_session_id} timezoneOffset=-180; {ts_id} {calypso_csrf} {calypso_csrf[:-1]}',
                'Origin': 'https://viavisolutions.wd1.myworkdayjobs.com',
                'Referer': 'https://viavisolutions.wd1.myworkdayjobs.com/careers?locations=992601fe562601082aa1272846780000',
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
                url='https://viavisolutions.wd1.myworkdayjobs.com/wday/cxs/viavisolutions/careers/jobs',
                method='POST',
                headers=headers,
                body=json.dumps(formdata),
                callback=self.parse
            )

    def parse(self, response):

        for job in response.json()["jobPostings"]:
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f'https://viavisolutions.wd1.myworkdayjobs.com/en-US/careers{job["externalPath"]}?locations=992601fe562601082aa1272846780000'
            item['job_title'] = job["title"]
            item['company'] = 'VIAVI'
            item['country'] = 'Romania'
            item['city'] = job["locationsText"].split(',')[0]
            item['logo_company'] = 'https://img.isemag.com/files/base/ebm/isemag/image/2022/12/viavi_descriptor_logo_cmyk_purple.6398b2849ee55.png?auto=format%2Ccompress&w=320'

            yield item
