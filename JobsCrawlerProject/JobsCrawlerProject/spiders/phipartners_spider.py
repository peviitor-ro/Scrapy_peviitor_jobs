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
import uuid


class PhipartnersSpiderSpider(CrawlSpider):
    name = "phipartners_spider"
    allowed_domains = ["www.phipartners.com"]
    start_urls = ["https://www.phipartners.com/careers/vacancies/"]

    rules = (
            Rule(LinkExtractor(allow=('/careers/vacancies/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):

        title = response.css('h1::text').get()
        location = response.css('div.post-hero__footer-item').get()

        if 'Vacancies' not in title and ('remote' in location.lower() or 'bucharest' in location.lower()):
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = response.url
            item['job_title'] = title
            item['company'] = 'PhiPartners'
            item['country'] = 'Romania'
            item['city'] = location.split('<strong>Location:</strong>')[-1].replace('</div>', '').strip()
            item['logo_company'] = 'https://www.finastra.com/sites/default/files/styles/small_hq/public/image/2023-05/logo-phi-partners.jpg?itok=zj7i5VcL'
            yield item
