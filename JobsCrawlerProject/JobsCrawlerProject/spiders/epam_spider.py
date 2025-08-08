import scrapy
from JobsCrawlerProject.items import JobItem

# personal scripts
from JobsCrawlerProject.get_job_type import get_job_type
from JobsCrawlerProject.found_county import get_county
from JobsCrawlerProject.__requests__ import get_curl_requests
import json


class EpamSpider(scrapy.Spider):
    name = "epam_spider"
    allowed_domains = ["epam.com", 'ip.me']
    start_urls = ["https://ip.me"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse_epam,
        )

    def parse_epam(self, response):

        print('aici')

        # make requests -> secret requests
        rrreqqq = get_curl_requests()
        req_json = rrreqqq.get(
            url = "https://www.epam.com/services/vacancy/search?locale=en&limit=100&recruitingUrl=%2Fcontent%2Fepam%2Fen%2Fcareers%2Fjob-listings%2Fjob&query=&country=Romania&sort=relevance&offset=0&searchType=placeOfWorkFilter&_=1752265205209",
            headers = {
                'accept': '*/*',
                'referer': 'https://www.epam.com/careers/job-listings?country=Romania',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
                },
                impersonate='chrome',
        )

        # extract data and sent it to peviitor DB
        json_data = json.loads(req_json.text)

        jobs = json_data.get('result')
        if jobs:
            for job in jobs:

                # town
                if (location := job.get('localizedCity')).lower() == 'bucharest':
                    location = 'Bucuresti'

                # location
                location_finish = get_county(location=location)

                # remote ---> data --->
                remote = None
                remote_brut = job.get('remote')
                if remote_brut == False:
                    remote = "on-site"
                else:
                    remote = 'remote'

                item = JobItem()
                item['job_link'] = job.get('url')
                item['job_title'] = job.get('name')
                item['company'] = 'EPAM'
                item['country'] = 'Romania'
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location
                item['remote'] = remote
                item['logo_company'] = ''
                #
                yield item
