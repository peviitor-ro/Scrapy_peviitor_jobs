#
#
#
#
#
# Company -> Suvoda
# Link ----> https://www.scania.com/ro/ro/home/about-scania/career/available-positions.html
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class SuvodaSpiderSpider(scrapy.Spider):
    name = "suvoda_spider"
    allowed_domains = ["boards.greenhouse.io"]
    start_urls = ["https://boards.greenhouse.io/embed/job_board?for=suvoda&b=https%3A%2F%2Fwww.suvoda.com%2Fcareers%2Fjob-openings"]

    def parse(self, response):
        
        for job in response.xpath('//div[@class="opening"]'):
            
            if (ro_location := job.xpath('.//span[@class="location"]//text()').extract_first())\
                                                            and 'romania' in ro_location.lower():
                
                ro_location = ro_location.split(',')[0]
                #
                location_finish = get_county(location=ro_location)

                # get items with new locations
                item = JobItem()
                item['job_link'] = job.xpath('.//a/@href').extract_first()
                item['job_title'] = job.xpath('.//a//text()').extract_first()
                item['company'] = 'Suvoda'
                item['country'] = 'Romania'
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if ro_location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != ro_location.lower()\
                                        else ro_location
                item['remote'] = 'on-site'
                item['logo_company'] = 'https://mma.prnewswire.com/media/1759317/4475440/Suvoda_Logo.jpg?p=twitter'
                #
                yield item
