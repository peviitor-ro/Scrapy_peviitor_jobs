#
#
#
#
# Company -> EWOR
# Link ----> https://join.com/companies/ewor?place%5B0%5D=
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class EworSpiderSpider(scrapy.Spider):
    name = "ewor_spider"
    allowed_domains = ["join.com"]
    start_urls = ['https://join.com/companies/ewor?place%5B0%5D=']

    def start_requests(self):

        cities = ['Bucharest',]
        for city in cities:

            # prepare url and headers for get request
            url = f'https://join.com/api/public/companies/33158/jobs?locale=en-us&filters%5Bplace%5D%5B0%5D={city}%2C%20Romania&page=1&pageSize=5&withAggregations=true&aggregateBy%5B0%5D=categoryId&aggregateBy%5B1%5D=place&sort=%2Btitle&isSpontaneousApplicationEnabled=true'

            headers = {  
                'authority': 'join.com',
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.8',
                'referer': 'https://join.com/companies/ewor?place%5B0%5D=',
                'release': 'job-ad-app@v12.0.1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                }
            
            yield scrapy.Request(
                url=url,
                method='GET',
                headers=headers,
                callback=self.parse_job
            )

    def parse_job(self, response):
        
        for job in response.json().get('items'):
            
            if (location := job.get('city').get('cityName')).lower() == 'bucharest':
                location = 'Bucuresti'

            location_finish = get_county(location=location)

            item = JobItem()
            item['job_link'] = "https://join.com/companies/ewor/" + job.get('idParam')
            item['job_title'] = job.get('title')
            item['company'] = 'EWOR'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                and True in location_finish and 'bucuresti' != location.lower()\
                                    else location
            item['remote'] = job.get('workplaceType').title()
            item['logo_company'] = 'https://cdn.join.com/61157a98f4fbb7000885977f/ewor-gmb-h-logo-xl.png'
            #
            yield item
