#
#
#
#
# Company -> JELLYSMACK
# Link ----> https://jobs.lever.co/jellysmack
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class JellysmackSpiderSpider(scrapy.Spider):
    name = "jellysmack_spider"
    allowed_domains = ["jobs.lever.co"]
    start_urls = ["https://jobs.lever.co/jellysmack"]

    def start_requests(self):
        yield scrapy.Request("https://jobs.lever.co/jellysmack")

    def parse(self, response):

        for job in response.css('div.posting'):
            city = job.css('div.posting')[0].css('span.sort-by-location.posting-category.small-category-label.location::text').get()

            if 'romania' in city.lower():
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('a.posting-title::attr(href)').get()
                item['job_title'] = job.css('h5::text').get()
                item['company'] = 'JELLYSMACK'
                item['country'] = 'Romania'
                item['city'] = city.split(',')[0]
                item['logo_company'] = 'https://blog.jellysmack.com/wp-content/uploads/sites/2/2022/04/Jellysmack-facts-logo-1024x263.png'

                yield item
