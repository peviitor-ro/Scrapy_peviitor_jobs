#
#
#
#
# Company -> Heimdal
# Link ----> https://heimdalsecurity.com/jobs
# Sec link-> https://heimdalsecurity.bamboohr.com/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class HeimdalSpiderSpider(scrapy.Spider):
    name = "heimdal_spider"
    allowed_domains = ["heimdalsecurity.com"]
    start_urls = ["https://heimdalsecurity.com/jobs"]

    custom_settings = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Refer': 'https://google.com',
            'DNT': '1'
        }

    def start_requests(self):
        yield scrapy.Request("https://heimdalsecurity.com/jobs")

    def parse(self, response):

        for idx, job in enumerate(response.css('div.row'), start=1):

            # excpet first 3 of elements
            if idx in [1, 2, 3]:
                continue

            elif idx > 9:
                break

            else:
                # start collect needed data here
                try:
                    link = job.css('a::attr(href)').get().strip()
                except:
                    link = '-'
                try:
                    title = job.css('h2::text').get().strip()
                except:
                    title = '-'
                try:
                    city = job.css('span.job-city::text').get().split()[0].strip()
                except:
                    city = '-'

                if city in ['Bucharest']:
                    item = JobItem()
                    item['id'] = str(uuid.uuid4())
                    item['job_link'] = link
                    item['job_title'] = title
                    item['company'] = 'Heimdal'
                    item['country'] = 'Romania'
                    item['city'] = city
                    item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiqqnZZ_xYO6q0r0l83olu79c9-_SFKI66j-mRym_B&s'
                    #
                    yield item
