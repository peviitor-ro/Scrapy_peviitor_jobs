#
#
#
#
# Company -> Aurachain
# Link ----> https://careers.aurachain.ch/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from scrapy.selector import Selector
#
from JobsCrawlerProject.found_county import get_county
#
import json


class AurachainSpiderSpider(scrapy.Spider):
    name = "aurachain_spider"
    allowed_domains = ["careers.aurachain.ch"]
    start_urls = ["https://careers.aurachain.ch/"]

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

        html_from_json_data = json.loads(response.text).get('html')
        
        # convert str to ScrapyObject
        selector = Selector(text=html_from_json_data)

        for link in selector.xpath('//a[contains(@href, "/job/")]/@href').extract():
            yield scrapy.Request(link, callback=self.parse_individal_page)

    # individual page
    def parse_individal_page(slef, response):

        if (location := response.xpath("//li[contains(@class, 'location')]/span[contains(@class, 'value')]/text()").extract_first().split(',')[0].lower()) == 'bucharest':
            location = 'Bucuresti'

        item = JobItem()
        item['job_link'] = response.url
        item['job_title'] = response.xpath("//div[contains(@class, 'heading')]/h2[contains(@class, 'title')]/text()").extract_first()
        item['company'] = 'Aurachain'
        item['country'] = 'Romania'
        item['county'] = get_county(location.title())
        item['city'] = location.title()
        item['remote'] = 'on-site'
        item['logo_company'] = 'https://careers.aurachain.ch/wp-content/uploads/2020/02/cropped-Aurachain-logo_v2.1-curent-Worksheet_Aurachain-logo3-e1564479066855.png'
        #
        yield item

