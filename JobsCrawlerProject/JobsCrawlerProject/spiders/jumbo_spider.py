#
#
#
#
# Company -> Jumbo
# Link ----> https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class JumboSpiderSpider(scrapy.Spider):
    name = "jumbo_spider"

    custom_settings = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    def start_requests(self):
        yield scrapy.Request("https://corporate.e-jumbo.gr/ro/job-opportunities/theseis-ergasias/")

    def parse(self, response):

        # data here
        for job in response.css('article.x-control.x-box.x-article-box.careers-article'):
            link = job.css('a::attr(href)').get().strip()
            title = job.css('h2::text').get().strip()

            if link and title:
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = 'https://corporate.e-jumbo.gr' + link
                item['job_title'] = title
                item['company'] = 'Jumbo'
                item['country'] = 'Romania'
                item['city'] = 'Romania'
                item['logo_company'] = 'https://corporate.e-jumbo.gr/uploads/images/logo.png'
                #
                yield item
