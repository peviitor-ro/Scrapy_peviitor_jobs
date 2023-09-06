#
#
#
#
# Company - PlaySolutions
# Link ----> https://play-solutions.ro/cariere/
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
import uuid


class PlaySolutionsSpider(CrawlSpider):
    name = "play-solutions"
    allowed_domains = ["play-solutions.ro"]
    start_urls = ["https://play-solutions.ro/cariere/"]

    rules = (
        Rule(
            LinkExtractor(allow=('/cariere/',)),
            callback='parse_job',
        ),
    )

    def parse_job(self, response):
        #
        title = response.css('h2.elementor-heading-title.elementor-size-default::text').get()
        if title:
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = response.url
            item['job_title'] = response.css('h2.elementor-heading-title.elementor-size-default::text').get()
            item['company'] = 'PlaySolutions'
            item['country'] = 'Romania'
            item['city'] = 'Remote'
            item['logo_company'] = 'https://play-solutions.ro/wp-content/uploads/2021/05/logo_play_header_blue.svg'
            yield item
