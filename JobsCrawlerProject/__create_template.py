#
#
#
#   Scrapy template creator
#   <--->
#   Author ---> Clarisse Braviceanu Badea
#
#   general template -> keyword: general
#   crawlspider template -> keyword: crawlspider
#   dynamic template -> keyword: dynamic
#
#   command: python3/python or py __create_template.py company_name link type_of_spider
#
import os
import sys

def make_general_spider(company_name: str, link: str) -> None:
    """
    General spider template.
    """

    spider_template = f"""
import scrapy
from JobsCrawlerProject.items import JobItem

# personal scripts
from JobsCrawlerProject.get_job_type import get_job_type
from JobsCrawlerProject.found_county import get_county


class {company_name.capitalize()}Spider(scrapy.Spider):
    name = "{company_name.lower()}_spider"
    allowed_domains = ["{link.replace('https://', '').replace('http://', '')}"]
    start_urls = ["{link}"]

    def parse(self, response):
        # search methods
        pass

        # Create item
        # item = JobItem()
        # item['job_link'] = ''
        # item['job_title'] = ''
        # item['company'] = '{company_name.upper()}'
        # item['country'] = 'Romania'
        # item['county'] = location_finish[0] if True in location_finish else None
        # item['city'] = 'all' if location.lower() == location_finish[0].lower()\\
        #             and True in location_finish and 'bucuresti' != location.lower()\\
        #                 else location
        # item['remote'] = ''
        # item['logo_company'] = ''
        # #
        # yield item
    """

    # Numele fișierului
    file_name = f"JobsCrawlerProject/spiders/{company_name.lower()}_spider.py"
    output_path = os.path.join(os.getcwd(), file_name)

    # Scrierea în fișier
    with open(output_path, mode='w', encoding='utf-8') as f:
        f.write(spider_template.strip())

    print(f"Spider script '{file_name}' generat cu succes la: {output_path}")


def make_crawlspider_template(company_name: str, link: str) -> None:
    """
    CrawlSpider template generator.
    """

    spider_template = f"""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class {company_name.capitalize()}Spider(CrawlSpider):
    name = "{company_name.lower()}_spider"
    allowed_domains = ["{link.replace('https://', '').replace('http://', '')}"]
    start_urls = ["{link}"]

    rules = (
        Rule(LinkExtractor(allow=(...,), deny=(...,)), callback='parse_job'),
    )

    def parse_job(self, response):
        # Logic for data extraction
        pass

        # item = JobItem()
        # item['job_link'] = ''
        # item['job_title'] = ''
        # item['company'] = '{company_name.upper()}'
        # item['country'] = 'Romania'
        # item['county'] = location_finish[0] if True in location_finish else None
        # item['city'] = 'all' if location.lower() == location_finish[0].lower()\\
        #             and True in location_finish and 'bucuresti' != location.lower()\\
        #                 else location
        # item['remote'] = ''
        # item['logo_company'] = ''
        # #
        # yield item
    """

    file_name = f"JobsCrawlerProject/spiders/{company_name.lower()}_spider.py"
    output_path = os.path.join(os.getcwd(), file_name)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', encoding='utf-8') as f:
        f.write(spider_template.strip())

    print(f"CrawlSpider script '{file_name}' generat cu succes la: {output_path}")


def make_playwright_spider_template(company_name: str, link: str) -> None:
    """
    Template generator for a Scrapy Spider with Playwright integration.
    """

    spider_template = f"""
import scrapy
#
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county
#
from scrapy.selector import Selector


class {company_name.capitalize()}Spider(scrapy.Spider):
    name = "{company_name.lower()}_spider"
    allowed_domains = ["{link.replace('https://', '').replace('http://', '')}"]
    start_urls = ["{link}"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={{
                "playwright": True,
            #     "playwright_page_methods": [
            #         {{"method": "wait_for_selector", "args": ['div.itemcard']}}
            #     ],
            #     "playwright_page_options": {{
            #         "timeout": 5000
            #     }}
            }}
        )

    def parse(self, response):
        # parse logic
        pass

        # item = JobItem()
        # item['job_link'] = ''
        # item['job_title'] = ''
        # item['company'] = '{company_name.upper()}'
        # item['country'] = 'Romania'
        # item['county'] = location_finish[0] if True in location_finish else None
        # item['city'] = 'all' if location.lower() == location_finish[0].lower()\\
        #             and True in location_finish and 'bucuresti' != location.lower()\\
        #                 else location
        # item['remote'] = ''
        # item['logo_company'] = ''
        # #
        # yield item
    """

    # Numele fișierului
    file_name = f"JobsCrawlerProject/spiders/{company_name.lower()}_spider.py"
    output_path = os.path.join(os.getcwd(), file_name)

    # Crearea directoarelor necesare
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Scrierea fișierului
    with open(output_path, mode='w', encoding='utf-8') as f:
        f.write(spider_template.strip())

    print(f"Spider script '{file_name}' generat cu succes la: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3/python or py create_scraper.py \"company_name\" \"link\" \"type_of_spider\" \"general/crawlspider/dynamic\"")
    else:
        company_name = sys.argv[1]
        link = sys.argv[2]
        type_of_spider = sys.argv[3]

        # Verificați dacă fișierul scraper există deja sau nu
        if os.path.exists(f'{company_name.lower()}_spider.py'):
            print(f"File {company_name.lower()}_spider.py already exists!")
        else:
            if type_of_spider == 'general':
                make_general_spider(company_name=company_name, link=link)
            elif type_of_spider == 'crawlspider':
                make_crawlspider_template(company_name=company_name, link=link)
            elif type_of_spider == 'dynamic':
                make_playwright_spider_template(company_name=company_name, link=link)
            else:
                print("Type of scraper needs to be 'general', 'crawlspider', 'dynamic'.")
