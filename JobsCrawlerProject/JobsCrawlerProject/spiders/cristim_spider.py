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
        if len(location := response.xpath('//p[contains(@class, "dmach-acf-value")\
                                       and contains(@class, "dmach-acf-video-container")]/text()').extract()) == 4:
            location = location[0]
        else:
            location = 'all'
        
        # get location
        location_finish = get_county(location=location)

        item = JobItem()
        item['job_link'] = response.url
        item['job_title'] = response.xpath('//h1[contains(@class, "entry-title") and contains(@class, "de_title_module")]/text()').extract_first()
        item['company'] = 'Cristim'
        item['country'] = 'Romania'
        item['county'] = (
                    'all' if 'all' in location_finish else
                    location_finish[0] if True in location_finish and isinstance(location_finish[0], str) else
                    None
                )
        item['city'] = 'all' if location.lower() == 'all' else location.title()
        item['remote'] = 'on-site'
        item['logo_company'] = 'https://cristim.ro/wp-content/uploads/2023/07/cropped-logo-pe-servet-600x600px_crop.jpg'
        yield item
