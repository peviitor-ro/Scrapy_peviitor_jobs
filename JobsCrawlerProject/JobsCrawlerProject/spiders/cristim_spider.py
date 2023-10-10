#
#
#
#
# Company -> Cristim
# Link ----> https://cristim.ro/cariere-cris-tim/
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
import uuid


class CristimSpiderSpider(CrawlSpider):
    name = "cristim_spider"
    allowed_domains = ["cristim.ro"]
    start_urls = ["https://cristim.ro/cariere-cris-tim/"]

    rules = (
            Rule(LinkExtractor(allow=('/cariere/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):
        item = JobItem()
        item['id'] = str(uuid.uuid4())
        item['job_link'] = response.url
        item['job_title'] = response.css('h1.entry-title.de_title_module.dmach-post-title::text').get().strip()
        item['company'] = 'Cristim'
        item['country'] = 'Romania'
        item['city'] = response.css('p.dmach-acf-value.dmach-acf-video-container::text').get().strip()
        item['logo_company'] = 'https://cristim.ro/wp-content/uploads/2023/07/cropped-logo-pe-servet-600x600px_crop.jpg'
        yield item
