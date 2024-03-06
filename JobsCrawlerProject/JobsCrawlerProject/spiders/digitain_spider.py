#
#
#
#
# Company -> Digitain
# Link ----> 
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county
#
import json
#
import requests


def prepare_post_requests(phpid: str, cfuvid: str) -> tuple:
    '''
    Prepare POST requests
    '''
    url = 'https://digitainsoftware.bamboohr.com/careers/list'

    headers = {
        'authority': 'digitainsoftware.bamboohr.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.5',
        'cookie': f'PHPSESSID={phpid}; _cfuvid={cfuvid}',
        'referer': 'https://digitainsoftware.bamboohr.com/careers',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    return url, headers


class DigitainSpiderSpider(scrapy.Spider):
    name = "digitain_spider"
    allowed_domains = ["www.digitain.com"]
    start_urls = ["https://www.digitain.com/career/"]

    def start_requests(self):

        # extract fresh cookies every time
        _cookies = requests.head('https://digitainsoftware.bamboohr.com/careers',
                                 headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X; ru-UA) AppleWebKit/537.36 (KHTML, like Gecko) Version/11.2.6 Mobile/15D100 Safari/537.36 Puffin/5.2.2IP'}).headers['Set-Cookie'].split()

        phpsessid = ''
        cfuvid = ''
        for ids in _cookies:
            if 'PHPSESSID' in ids:
                phpsessid = ids
            if 'cfuvid' in ids:
                cfuvid = ids

        url, headers = prepare_post_requests(phpsessid, cfuvid)

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):

        for job in response.json().get('result'):

            if str((location := job.get('location').get('city'))).lower() == 'bucharest':
                location = 'Bucuresti'

                location_finish = get_county(location=location.title())
            
                # parse items here
                item = JobItem()
                item['job_link'] = f'https://digitainsoftware.bamboohr.com/careers/{job.get("id")}'
                item['job_title'] = job.get('jobOpeningName')
                item['company'] = 'Digitain'
                item['country'] = 'Romania'
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location
                item['remote'] = 'remote' if job.get('isRemote') != None else 'on-site'
                item['logo_company'] = 'https://cristim.ro/wp-content/uploads/2023/07/cropped-logo-pe-servet-600x600px_crop.jpg'
                yield item
