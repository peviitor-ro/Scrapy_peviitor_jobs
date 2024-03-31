#
#
#
#
# Company -> Signicat
# Link ----> https://www.signicat.com/about/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from typing import Union


class SignicatSpiderSpider(scrapy.Spider):
    name = "signicat_spider"
    allowed_domains = ["www.signicat.com"]
    start_urls = ["https://signicat.teamtailor.com/jobs"]

    def parse(self, response):

        for job in response.xpath('//li[@class="w-full"]'):
            #
            ro_location = [x.strip() for x in
                        job.xpath('.//div[contains(@class, "mt-1") and contains(@class, "text-md")]//text()').extract()
                        if x.strip() and x != '·']
            
            # get f****** job type
            job_type: Union[str, list] = None
            check_for_remote = ro_location[-1].lower()
            if 'remote' and 'hybrid' in check_for_remote:
                job_type = ['hybrid', 'remote',]
            elif 'remote' in check_for_remote:
                job_type = 'remote'
            elif 'hybrid' in check_for_remote:
                job_type = 'hybrid'
            else:
                job_type = 'on-site'
            #
            if ro_location and 'romania' in ro_location[1].lower():
                item = JobItem()
                item['job_link'] = job.xpath('.//a/@href').extract_first()
                item['job_title'] = [xx.strip() for xx in
                                    job.xpath('.//a//text()').extract()
                                    if xx.strip()][0]
                item['company'] = 'Signicat'
                item['country'] = 'Romania'
                item['county'] = 'Bucuresti'
                item['city'] = 'Bucuresti'
                item['remote'] = job_type
                item['logo_company'] = 'https://images.teamtailor-cdn.com/images/s3/teamtailor-production/logotype-v3/image_uploads/cbd19f90-5af8-4896-b889-d91ab4f32b07/original.png'

                yield item

