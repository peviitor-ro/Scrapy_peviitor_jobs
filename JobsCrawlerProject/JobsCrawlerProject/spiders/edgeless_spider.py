#
#
#
#
# Company -> EdgeLess
# Link ----> http://www.edgeless.ro/careers/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class EdgelessSpiderSpider(scrapy.Spider):
    name = "edgeless_spider"
    allowed_domains = ["www.edgeless.ro"]
    start_urls = ["http://www.edgeless.ro/careers/#jobs"]

    def start_requests(self):
        yield scrapy.Request("http://www.edgeless.ro/careers/")

    def parse(self, response):

        # parse links to jobs here
        for job in response.css('div.elementor-flip-box__layer__inner'):

            if (link := job.css('a.elementor-flip-box__button.elementor-button.elementor-size-sm::attr(href)').get()):
                yield scrapy.Request(url=link, callback=self.parse_job_details)

    def parse_job_details(self, response):

        # parse data and send it to pipelines.py
        item = JobItem()
        item['id'] = str(uuid.uuid4())
        item['job_link'] = response.url
        item['job_title'] = response.css('h1::text')[1].get()
        item['company'] = 'EdgeLess'
        item['country'] = 'Romania'
        item['city'] = response.css('div.elementor-widget-container > ul').css('li:contains("Location:") em span::text').get()
        item['logo_company'] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXKx4pqVnhEvKxETB_rWvem5yJpmEv_jkNaM2eGHsK0w&s'
        #
        yield item
