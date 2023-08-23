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
