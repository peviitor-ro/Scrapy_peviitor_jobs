#
#
#
#
# Company -> Globant
# Link ----> https://career.globant.com/
#
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class GlobantSpiderSpider(CrawlSpider):
    name = "globant_spider"
    allowed_domains = ["career.globant.com"]
    start_urls = ["https://career.globant.com/search/?createNewAlert=false&q=&optionsFacetsDD_department=&optionsFacetsDD_country=RO"]

    rules = (
            Rule(LinkExtractor(allow=('/job/',), deny=('/apply',)),
                 callback='parse_job'),
            )

    def parse_job(self, response):

        # get location
        location = response.xpath('//span[@class="jobGeoLocation"]/text()').extract()[0].strip().split(',')
        #
        search_elements = [element.lower().strip() for element in location]
        
        # get exact location
        if (exact_location := location[0].strip()).lower() == "other city":
            exact_location == 'All'
        else:
            exact_location = location[0].strip()

        # get job type
        job_type = ''
        if 'hybrid' in search_elements:
            job_type = 'hybrid'
        elif 'remote' in search_elements:
            job_type = 'remote'

        # get data
        if 'ro' in search_elements:
            #
            # parse data here
            item = JobItem()
            item['job_link'] = response.url
            item['job_title'] = response.xpath('//h1[@id="job-title"]/text()').extract_first()
            item['company'] = 'Globant'
            item['country'] = 'Romania'
            item['county'] = "All" if get_county(exact_location) == None else get_county(location[0].strip())
            item['city'] = 'All' if exact_location.lower() == "other city" else location[0].strip()
            item['remote'] = job_type
            item['logo_company'] = 'https://www.globant.com/themes/custom/globant_corp_theme/images/2019/globant-logo-dark.svg'
            yield item
