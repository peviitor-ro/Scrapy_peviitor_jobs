#
#
#
#
# Company -> Hutchinson
# Link ----> https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1007
#
import scrapy
#
from JobsCrawlerProject.items import JobItem
#
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
#
import uuid


class HutchinsonSpiderSpider(scrapy.Spider):
    name = "hutchinson_spider"

    allowed_domains = ["fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com"]
    start_urls = ["https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1007/requisitions?location=Romania&locationId=300000000378617&locationLevel=country&mode=location"]

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
            await page.wait_for_selector('div.job-list-item__content', state='visible')

            while True:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await page.wait_for_timeout(1000)

                can_scroll = await page.evaluate('''() => {
                    const scrollTop = window.pageYOffset;
                    const scrollHeight = document.body.scrollHeight;
                    const clientHeight = document.documentElement.clientHeight;
                    return scrollHeight > scrollTop + clientHeight;
                }''')

                if not can_scroll:
                    break

            dynamic_content = await page.inner_html('body')

            await page.close()
            await context.close()
            await browser.close()

            # scrape all jobs
            soup = BeautifulSoup(dynamic_content, 'lxml')
            soup_data = soup.find_all('a', attrs={'class': 'job-list-item__link'})

            for job in soup_data:
                link = job['href']
                title = job.find('span', attrs={'class': 'job-tile__title'}).text
                city = job.select_one('span[data-bind="html: primaryLocation"]').text.split(',')[0]

                print(link, title, city)

                if link and title:
                    item = JobItem()
                    item['id'] = str(uuid.uuid4())
                    item['job_link'] = link
                    item['job_title'] = title
                    item['company'] = 'Hutchinson'
                    item['country'] = 'Romania'
                    item['city'] = city
                    item['logo_company'] = 'https://floatmast.com/wp-content/uploads/2021/04/logo-hutchinson-1260x709.jpg'
                    #
                    yield item
