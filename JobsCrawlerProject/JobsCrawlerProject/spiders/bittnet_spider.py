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
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
#
import uuid
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
            soup = BeautifulSoup(dynamic_content, 'lxml')
            soup_data = soup.find_all('div', attrs={'class': 'row-item'})

            # here parse jobs
            for job in soup_data:
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = 'https://www.bittnet.jobs' + job.find('a')['href'].strip()
                item['job_title'] = job.find('a').text.strip()
                item['company'] = 'Bittnet'
                item['country'] = 'Romania'
                item['city'] = re.split(r'(?=[A-Z])', str(job.text.split()[-1]))[-1]
                item['logo_company'] = 'https://www.bittnet.jobs/img/logo_ro.png'
                #
                yield item
