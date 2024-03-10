#
#
#
#
# Company -> yPhiPartners
# Link ----> https://www.phipartners.com/careers/vacancies/
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class PhipartnersSpiderSpider(CrawlSpider):
    name = "phipartners_spider"
    allowed_domains = ["www.phipartners.com"]
    start_urls = ["https://www.phipartners.com/careers/vacancies/"]

    rules = (
            Rule(LinkExtractor(allow=('/careers/vacancies/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):

        title = response.xpath('//h1/text()').extract_first()
        location_list = [elem.strip() for elem\
                            in response.xpath('//div[@class="post-hero__footer-item"]//text()').extract()\
                                if elem.strip()]

        if 'Vacancies' not in title\
                and ('remote' in str(location_list).lower()\
                     or 'bucharest' in str(location_list).lower()):

            # get romanian name for city
            if (location := location_list[1].split(',')[0].lower()) == 'bucharest':
                location = 'Bucuresti'

            # get location finish algorithm
            location_finish = get_county(location=location)

            item = JobItem()
            item['job_link'] = response.url
            item['job_title'] = title
            item['company'] = 'PhiPartners'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                and True in location_finish and 'bucuresti' != location.lower()\
                                    else location
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://www.finastra.com/sites/default/files/styles/small_hq/public/image/2023-05/logo-phi-partners.jpg?itok=zj7i5VcL'
            yield item
