#
#
#
#
# Company -> Aurachain
# Link ----> https://careers.aurachain.ch/
#
import scrapy
from scrapy.http import FormRequest
from JobsCrawlerProject.items import JobItem
#
from bs4 import BeautifulSoup
#
import uuid
import json


class AurachainSpiderSpider(scrapy.Spider):
    name = "aurachain_spider"
    allowed_domains = ["careers.aurachain.ch"]
    start_urls = ["https://careers.aurachain.ch/"]

    custom_settings = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    def start_requests(self):

        # prepare data row and headers for post requests
        formdata = {
                'lang': '',
                'search_keywords': '',
                'search_location': '',
                'filter_job_type[]': ['contract-based', 'freelance', 'full-time', 'internship', 'part-time', 'temporary', ''],
                'per_page': '13',
                'orderby': 'featured',
                'order': 'DESC',
                'page': '1',
                'show_pagination': 'false',
                'form_data': 'search_keywords=&search_location=&search_region=0&filter_job_type%5B%5D=contract-based&filter_job_type%5B%5D=freelance&filter_job_type%5B%5D=full-time&filter_job_type%5B%5D=internship&filter_job_type%5B%5D=part-time&filter_job_type%5B%5D=temporary&filter_job_type%5B%5D='
            }
        headers = {
            'authority': 'careers.aurachain.ch',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://careers.aurachain.ch',
            'referer': 'https://careers.aurachain.ch/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            }

        yield scrapy.Request(
                url='https://careers.aurachain.ch/jm-ajax/get_listings/',
                method='POST',
                headers=headers,
                body=json.dumps(formdata),
                callback=self.parse
            )

    def parse(self, response):

        # make soup object for html from json
        soup = BeautifulSoup(response.json()['html'], 'lxml')
        soup_data = soup.find_all('li', attrs={'class': 'job_listing'})

        for job in soup_data:

            city = job.find('div', attrs={'class': 'location'}).text.strip()

            # check for location
            if 'romania' in city.lower():

                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.find('a')['href']
                item['job_title'] = job.find('h3').text
                item['company'] = 'Aurachain'
                item['country'] = 'Romania'
                item['city'] = city.split(',')[0].strip()
                item['logo_company'] = 'https://aurachain.ch/wp-content/uploads/2022/12/Aurachain-logo_svg-06.svg'

                yield item
