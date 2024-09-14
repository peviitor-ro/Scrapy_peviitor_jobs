#
#
#
# Playwright
# Company -> Bittnet
# Link ----> https://www.bittnet.jobs/1048/lista-posturi
#
from os import stat_result
from typing_extensions import Text
import scrapy
#
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county
#
from playwright.async_api import async_playwright
from scrapy.selector import Selector
#
import re


class BittnetSpiderSpider(scrapy.Spider):
    name = "bittnet_spider"
    allowed_domains = ["www.bittnet.jobs"]
    start_urls = ["https://www.bittnet.jobs/1048/lista-posturi"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    {"method": "wait_for_selector", "args": ['div.itemcard']}
                ],
                "playwright_page_options": {
                    "timeout": 5000
                }
            }
        )

    def parse(self, response):

        jobs_items_card = response.xpath('//div[@class="itemcard"]')

        # extract data from jobs_items_crad: link, title, location
        for job_item in jobs_items_card:

            location = job_item.xpath('.//div[@class="row-item"]//text()').extract()

            # if location - en
            location = location[-1]
            if location.lower() == 'bucharest':
                location = 'Bucuresti'

            location_finish = get_county(location=location)

            if (title := job_item.xpath('.//div[@class="row-item"]/a/text()').get()):

                item = JobItem()
                item['job_link'] = "https://www.bittnet.jobs" + job_item.xpath('.//div[@class="row-item"]/a/@href').get()
                item['job_title'] = title
                item['company'] = 'Bittnet'
                item['country'] = 'Romania'
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location
                item['remote'] = 'on-site'
                item['logo_company'] = 'https://www.bittnet.jobs/img/logo_ro.png'
                #
                yield item
