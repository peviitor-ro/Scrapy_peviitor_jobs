#
#
#
#
# Company -> Teamland
# Link ----> https://www.teamland.ro/j.php?_=1686681054574
#
from bs4 import BeautifulSoup
import scrapy
from JobsCrawlerProject.found_county import get_county
from JobsCrawlerProject.items import JobItem


class TeamlandSpiderSpider(scrapy.Spider):
    name = "teamland_spider"
    allowed_domains = ["teamland.ro"]
    start_urls = ["https://www.teamland.ro/j.php?_=1686681054574"]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        yield scrapy.Request(url=self.start_urls[0], method='GET', headers=headers, callback=self.parse)

    def parse(self, response):
        # Load the JSON data
        data = response.json().get('data', [])

        for job in data:
            link_id = job[0]
            title = BeautifulSoup(job[1], 'lxml').find('span').text.strip()
            location = BeautifulSoup(job[2], 'lxml').find('span').text.strip()
            location_finish = get_county(location=location)

            item = JobItem()
            item['job_link'] = f"https://www.teamland.ro/apply.php?id={link_id}#content"
            item['job_title'] = title
            item['company'] = 'Teamland'
            item['country'] = 'Romania'
            item['city'] = location
            item['county'] = location_finish[0] if True in location_finish else None
            item['remote'] = 'remote' if 'remote' in location.lower() else 'on-site'
            item['logo_company'] = 'https://www.teamland.ro/img/logo.png'
            yield item
