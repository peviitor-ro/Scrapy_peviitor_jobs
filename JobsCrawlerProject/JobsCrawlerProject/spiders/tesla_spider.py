#
#
#
#
#
import scrapy
from JobsCrawlerProject.items import JobItem


class TeslaSpiderSpider(scrapy.Spider):
    name = "tesla_spider"
    allowed_domains = ["www.tesla.com"]
    start_urls = ['https://www.tesla.com/cua-api/apps/careers/state']

    # disable robots.txt for Tesla
    custom_settings = {
            'ROBOTSTXT_OBEY': False
        }
    
    def start_requests(self):
        '''
        Start Request to Tesla API -> Scrape all data from one request
        '''

        headers = {
            'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.tesla.com/careers/search',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Linux"',
        }

        yield scrapy.Request(url=self.start_urls[0],
                             headers=headers,
                             method='GET',
                             callback=self.parse,)
    
    def parse(self, response):
        
        # get ids for search data in Tesla API
        ids = dict()
        try:
            if (_id := response.json().get('geo')[1].get('sites')[23])\
                and _id.get('id').lower() == 'ro':
                #
                ids.update(_id.get('cities'))
        except:
            if (_id := response.json().get('geo')[1].get('sites')[24])\
                and _id.get('id').lower() == 'ro':
                #
                ids.update(_id.get('cities'))

        # search jobs data in API with our kyes for GeoLocations
        for job_search in response.json().get('listings'):
            for k, v in ids.items():
                for j in v:
                    if j == job_search.get('l'):
                    
                        # get items with new locations
                        item = JobItem()
                        item['job_link'] = f"https://www.tesla.com/careers/search/job/{job_search.get('id')}"
                        item['job_title'] = job_search.get('t')
                        item['company'] = 'Tesla'
                        item['country'] = 'Romania'
                        item['county'] = ''
                        item['city'] = k
                        item['remote'] = 'on-site'
                        item['logo_company'] = 'https://i.ebayimg.com/images/g/bfUAAOSw88RbDbfe/s-l1600.jpg'
                        #
                        yield item