#
#
#
#
# Company -> Google
# Link ----> https://www.google.com/about/careers/applications/jobs/results/?distance=50&has_remote=false&hl=en_US&jlo=en_US&location=Romania&q=
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county


class GoogleSpiderSpider(scrapy.Spider):
    name = "google_spider"
    allowed_domains = ["careers.google.com"]
    start_urls = ["https://careers.google.com/jobs/results/?distance=50&has_remote=false&hl=en_US&jlo=en_US&location=Romania&q="]

    def start_requests(self):
        url = 'https://careers.google.com/api/v3/search/?distance=50&has_remote=false&hl=en_US&jlo=en_US&location=Romania&q='
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        yield scrapy.Request(url=url, method='GET', headers=headers, callback=self.parse)

    def parse(self, response):
        jobs = response.json().get('jobs', [])

        for job in jobs:
            city = job['locations'][0]['city']

            if str(city).lower() == 'bucharest':
                city = 'Bucuresti'

            location_finish = get_county(location=city.title())

            # Parse job item
            item = JobItem()
            item['job_link'] = f"https://careers.google.com/jobs/results/{job['id'][5:]}-{'-'.join(job['title'].replace(',', '').replace('(', '').replace(')', '').lower().split())}/?location=Romania"
            item['job_title'] = job['title']
            item['company'] = 'Google'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if city.lower() == location_finish[0].lower() and True in location_finish and 'bucuresti' != city.lower() else city
            item['remote'] = 'remote' if 'remote' in job.get('title', '').lower() else 'on-site'
            item['logo_company'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/250px-Google_2015_logo.svg.png'
            yield item
