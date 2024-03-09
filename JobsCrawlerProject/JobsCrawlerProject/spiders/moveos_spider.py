#
#
#
#
# Company -> Moveos
# Link ----> https://www.hr.moveos.ro/en/jobs/
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class MoveosSpiderSpider(scrapy.Spider):
    name = "moveos_spider"
    allowed_domains = ["www.hr.moveos.ro"]
    start_urls = ["https://moveos.ro/locuri-de-munca?start="]

    def start_requests(self):
        page = 0
        while True:
            yield scrapy.Request(self.start_urls[0] + str(page))

            page += 9

    def parse(self, response):

        if len(check_valid_data_from_page := response.xpath('//div[@class="locuri-de-munca"]')) > 0:
            
            for job in check_valid_data_from_page:
                if job.xpath('.//div[@class="anunt-inactiv"]/p/text()').extract_first() is None:
                    #
                    location = job.xpath('.//div[@class="locuri-de-munca-detalii"]//text()').extract_first()
                    location_finish = get_county(location=location)
                    #
                    item = JobItem()
                    item['job_link'] = "https://moveos.ro" +job.xpath('.//div[@class="readmore"]//a/@href').extract_first()
                    item['job_title'] = job.xpath('.//h2[contains(@itemprop, "headline")]//text()').extract_first()
                    item['company'] = 'Moveos'
                    item['country'] = 'Romania'
                    item['county'] = location_finish[0] if True in location_finish else None
                    item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                        and True in location_finish and 'bucuresti' != location.lower()\
                                            else location
                    item['remote'] = 'on-site'
                    item['logo_company'] = 'https://moveos.ro/images/logo_moveos_final-v2.svg'
                    #
                    yield item
                else:
                    self.crawler.engine.close_spider(self, 'No valid data found')
        
        # stop crawler
        else:
            self.crawler.engine.close_spider(self, 'No valid data found')
