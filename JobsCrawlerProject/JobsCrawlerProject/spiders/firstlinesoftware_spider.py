#
#
#
#
# Company -> FirstLineSoftware
# Link ----> https://careers.firstlinesoftware.com/en/
#
import scrapy
from JobsCrawlerProject.items import JobItem
from bs4 import BeautifulSoup
#
import uuid


class FirstlinesoftwareSpiderSpider(scrapy.Spider):
    name = "firstlinesoftware_spider"
    allowed_domains = ["careers.firstlinesoftware.com"]
    start_urls = ["https://careers.firstlinesoftware.com/en/"]

    def start_requests(self):
        page = 0
        while True:
            yield scrapy.Request(f'https://careers.firstlinesoftware.com/wp-admin/admin-ajax.php?action=alm_get_posts&query_type=standard&id=&post_id=0&slug=home&canonical_url=https:%2F%2Fcareers.firstlinesoftware.com%2Fen%2F&posts_per_page=4&page={page}&offset=0&post_type=vacancies&repeater=default&seo_start_page=1&lang=en&category__and=69&order=DESC&orderby=date', callback=self.parse)
            page += 1

    def parse(self, response):

        if response.json()["html"] is not None:
            # parse html from json
            soup = BeautifulSoup(response.json()["html"], 'lxml')
            soup_data = soup.find_all('div', attrs={'class': 'pl_jobs-box'})

            for job in soup_data:
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.find('a')['href']
                item['job_title'] = job.find('div', attrs={'class': 'jobs-item-content-name h4 bind'}).text
                item['company'] = 'FirstLineSoftware'
                item['country'] = 'Romania'
                item['city'] = 'Remote'
                item['logo_company'] = 'https://careers.firstlinesoftware.com/wp-content/themes/fls_poland_career/assets/images/logo.png'
                #
                yield item
        else:
            self.log(f"Page {response.url} doesn't contain data. Stopping iteration.")
            self.crawler.engine.close_spider(self, "No more data")
