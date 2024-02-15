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
from JobsCrawlerProject.found_county import get_county


class CristimSpiderSpider(CrawlSpider):
    name = "cristim_spider"
    allowed_domains = ["cristim.ro"]
    start_urls = ["https://cristim.ro/cariere-cris-tim/"]

    rules = (
            Rule(LinkExtractor(allow=('/cariere/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):

        # scrape location here... because it used in two places
        location = response.xpath('//p[contains(@class, "dmach-acf-value") and contains(@class, "dmach-acf-video-container")]/text()').extract()[0]

        item = JobItem()
        item['job_link'] = response.url
        item['job_title'] = response.xpath('//h1[contains(@class, "entry-title") and contains(@class, "de_title_module")]/text()').extract_first()
        item['company'] = 'Cristim'
        item['country'] = 'Romania'
        item['county'] = get_county(location)
        item['city'] = response.css('p.dmach-acf-value.dmach-acf-video-container::text').get().strip()
        item['remote'] = 'on-site'
        item['logo_company'] = 'https://cristim.ro/wp-content/uploads/2023/07/cropped-logo-pe-servet-600x600px_crop.jpg'
        yield item
