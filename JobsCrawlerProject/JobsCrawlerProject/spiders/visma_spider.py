
#
#
#
#
# Company Visma
# https://www.visma.com/careers/open-positions
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class VismaSpiderSpider(scrapy.Spider):
    name = "visma_spider"
    allowed_domains = ["visma.com"]
    start_urls = ["https://www.visma.com/careers/open-positions"]

    def parse(self, response):
        #
        for job in response.xpath('//div[@class="content_card"]'):
            #
            if (country_ro := job.xpath(".//div[@fs-cmssort-field='locationtext']//text()").extract())\
                                        and country_ro[0].lower() == 'romania':
                #
                location_s = [town.strip() for town in country_ro[1].replace('| ', '').split(',')]
                #
                location_finish = [get_county(location=x_loc) for x_loc in location_s]
                counties_true = [xx[0] if True in xx else None for xx in location_finish]
                #
                item = JobItem()
                item['job_link'] = job.xpath('.//a[contains(@class, "apply-button")]/@href').extract_first()
                item['job_title'] = job.xpath(".//div[@fs-cmssort-field='title']//text()").extract_first()
                item['company'] = 'Visma'
                item['country'] = 'Romania'
                item['county'] = None if None in counties_true else counties_true
                item['city'] = location_s[0] if len(location_s) == 1 else location_s
                item['remote'] = 'hybrid'
                item['logo_company'] = 'https://vectorlogoseek.com/wp-content/uploads/2019/02/visma-vector-logo.png'

                yield item
