#
#
#
#
# Company -> Heimdal
# Link ----> https://heimdalsecurity.com/jobs
# Sec link-> 
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county
#
import requests


def get_cookie():
    '''
    ... get headers with requests... not work with Scrapy
    '''
    phpses = ''
    cf__ = ''
    for data in requests.head('https://heimdalsecurity.bamboohr.com/careers').headers.get('Set-Cookie').split():
        if 'PHPSESSID' in data:
            phpses = data
        elif '_cfuvid' in data:
            cf__ = data

    return phpses, cf__


class HeimdalSpiderSpider(scrapy.Spider):
    name = "heimdal_spider"
    allowed_domains = ["heimdalsecurity.com"]
    start_urls = ["https://heimdalsecurity.bamboohr.com/careers/list"]

    def start_requests(self):

        # call func for phpsesid and cf
        phpsession, cf__ = get_cookie()
        headers = {
            'authority': 'heimdalsecurity.bamboohr.com',
            'accept': 'application/json, text/plain, */*',
            'cookie': f'notice_behavior=expressed|eu; {phpsession} {cf__[:-1]}',
            'referer': 'https://heimdalsecurity.bamboohr.com/careers',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }


        yield scrapy.Request(url=self.start_urls[0],
                             callback=self.parse_headers,
                             headers=headers,
                             method='GET',
                             )

    def parse_headers(self, response):
        
        for job in response.json().get('result'):
            new_loc = ''
            if (location := job.get('location').get('city')) != None:
                if location.lower() == 'bucharest':
                    new_loc = 'Bucuresti'
            elif (country := job.get('atsLocation').get('country')) != None:
                    if country.lower() == 'romania' and job.get('atsLocation').get('city').lower() == 'all cities':
                        new_loc = 'All'
            else:
                continue

            job_type = ''
            if new_loc.lower() != 'all':
                job_type = 'hybryd'
            else:
                job_type = 'remote'

            location_finish = get_county(location=new_loc)

            if new_loc:
                item = JobItem()
                item['job_link'] = f"https://heimdalsecurity.bamboohr.com/careers/{job.get('id')}"
                item['job_title'] = job.get('jobOpeningName')
                item['company'] = 'Heimdal'
                item['country'] = 'Romania'
                item['county'] = (
                    'all' if 'all' in location_finish else
                    location_finish[0] if True in location_finish and isinstance(location_finish[0], str) else
                    None
                )
                item['city'] = 'all' if new_loc.lower() == 'all' else new_loc.title()
                item['remote'] = job_type
                item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiqqnZZ_xYO6q0r0l83olu79c9-_SFKI66j-mRym_B&s'
                #
                yield item