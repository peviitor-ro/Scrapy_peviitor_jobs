#
#
#
#
# Company -> LILT
# Link ----> https://jobs.ashbyhq.com/lilt
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county
#
from playwright.async_api import async_playwright
#
from scrapy.selector import Selector


class LiltSpiderSpider(scrapy.Spider):
    name = "lilt_spider"
    allowed_domains = ["jobs.ashbyhq.com"]
    start_urls = ["https://jobs.ashbyhq.com/lilt"]

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

            # now extract all data with scrapy.Selector
            selector = Selector(text=dynamic_content)

            for job in selector.xpath('//a[contains(@class, "_container_j2da7_1")]'):
                
                if (city := job.xpath('.//div[contains(@class, "_details_1qwfy_389")\
                                      and contains(@class, "ashby-job-posting-brief-details")]//p/text()').extract()):
                    
                    # check if romania in loc()
                    if 'romania' in str([elem.lower() for elem in city]):
                        item = JobItem()
                        item['job_link'] = 'https://jobs.ashbyhq.com' + job.xpath('./@href').extract_first()
                        item['job_title'] = job.xpath('.//h3[contains(@class, "_title_1qwfy_383")]//text()').extract_first()
                        item['company'] = 'LILT'
                        item['country'] = 'Romania'
                        item['county'] = ''
                        item['city'] = ''
                        item['remote'] = 'on-site'
                        item['logo_company'] = 'https://app.ashbyhq.com/api/images/org-theme-wordmark/e47e9e25-ae9f-4031-85fd-42d02e602221/330a7ebd-cd46-41e2-997b-775c9bf7255e.png'
                        #
                        yield item
