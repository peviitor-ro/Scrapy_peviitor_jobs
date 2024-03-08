#
#
#
# Playwright
# Company -> Bittnet
# Link ----> https://www.bittnet.jobs/1048/lista-posturi
#
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

    @classmethod
    async def parse(cls, response):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(response.url)
            await page.wait_for_load_state('domcontentloaded')

            # wait for selector
            await page.wait_for_selector('div.itemcard', state='visible')

            dynamic_content = await page.inner_html('body')

            await page.close()
            await context.close()
            await browser.close()

            # scrape all jobs
            selector = Selector(text=dynamic_content)

            # here parse jobs
            for job in selector.xpath('//div[contains(@class, "itemcard")]'):

                # get location
                location = job.xpath('//div[@class="row-item"]/text()').extract_first()

                location_finish = get_county(location=location)

                item = JobItem()
                item['job_link'] = "https://www.bittnet.jobs" + job.xpath('//div[@class="row-item"]/a/@href').get()
                item['job_title'] = job.xpath('//div[@class="row-item"]/a/text()').get()
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