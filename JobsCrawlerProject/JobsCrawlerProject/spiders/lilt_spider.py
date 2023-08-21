#
#
#
#
# Company -> LILT
# Link ----> https://jobs.ashbyhq.com/lilt
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from playwright.async_api import async_playwright
#
from bs4 import BeautifulSoup
#
import uuid


class LiltSpiderSpider(scrapy.Spider):
    name = "lilt_spider"
    allowed_domains = ["jobs.ashbyhq.com"]
    start_urls = ["https://jobs.ashbyhq.com/lilt"]

    custom_settings = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    @classmethod
    async def parse(cls, response):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(response.url)
            await page.wait_for_load_state('domcontentloaded')

            # wait for selector
            await page.wait_for_selector('h3', state='visible')

            dynamic_content = await page.inner_html('body')

            await page.close()
            await context.close()
            await browser.close()

            # now extract all data with bs4!
            soup = BeautifulSoup(dynamic_content, 'lxml')
            soup_data = soup.find_all('a', attrs={'class': '_container_j2da7_1'})

            for job in soup_data:
                city = job.find('div', attrs={'class': 'ashby-job-posting-brief-details'}).find('p').text.strip()

                if 'romania' in city.lower():
                    item = JobItem()
                    item['id'] = str(uuid.uuid4())
                    item['job_link'] = 'https://jobs.ashbyhq.com' + job['href'].strip()
                    item['job_title'] = job.find('h3', attrs={'class': 'ashby-job-posting-brief-title'}).text.strip()
                    item['company'] = 'LILT'
                    item['country'] = 'Romania'
                    item['city'] = 'Romania'
                    item['logo_company'] = 'https://app.ashbyhq.com/api/images/org-theme-wordmark/e47e9e25-ae9f-4031-85fd-42d02e602221/330a7ebd-cd46-41e2-997b-775c9bf7255e.png'
                    #
                    yield item
