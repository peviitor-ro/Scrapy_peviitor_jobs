#
#
#
#
# Company -> Centric
# Link ----> https://careers.centric.eu/ro/open-positions/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid
#
import re
import json
from bs4 import BeautifulSoup


class CentricSpiderSpider(scrapy.Spider):
    name = "centric_spider"
    allowed_domains = ["careers.centric.eu"]
    start_urls = ["https://careers.centric.eu/ro/open-positions/"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        pattern = r'window\.FILTER_BAR_INITIAL\s*=\s*({.*?});'
        match = re.search(pattern, response.text)

        if match:
            filter_bar_initial = match.group(1)
            parse_filter = json.loads(filter_bar_initial)

            # parse data from filter with BS4
            for job in parse_filter["results"]:
                soup = BeautifulSoup(job, "lxml")

                loc = soup.find('div')["data-location"]

                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = soup.find('a', attrs={"class": "card__anchor"})["href"]
                item['job_title'] = soup.find('div', attrs={"class": "card__title"}).text
                item['company'] = 'Centric'
                item['country'] = 'Romania'
                item['city'] = loc
                item['logo_company'] = 'https://careers.centric.eu/static/images/logo.svg'
                yield item

        else:
            print("Variabila window.FILTER_BAR_INITIAL nu a fost găsită.")
