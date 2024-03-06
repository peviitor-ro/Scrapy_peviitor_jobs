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
        if bool(location := response.xpath('//span[@class="jobGeoLocation"]/text()').extract()):

            search_elements = [element.strip().lower() for element in location[0].split(',')]

            # get exact location
            if (exact_location := search_elements[0].strip().lower()) == "other city":
                exact_location = 'all'
            else:
                exact_location = search_elements[0]

            # get job type
            job_type = ''
            if 'hybrid' in location[0].lower():
                job_type = 'hybrid'
            elif 'remote' in location[0].lower():
                job_type = 'remote'
            else:
                job_type = 'on-site'

            # get data
            if 'ro' in search_elements:

                location_finish  = get_county(location=exact_location)
                #
                # parse data here
                item = JobItem()
                item['job_link'] = response.url
                item['job_title'] = response.xpath('//h1[@id="job-title"]/text()').extract_first()
                item['company'] = 'Globant'
                item['country'] = 'Romania'
                item['county'] = location_finish[0] if True in location_finish else None
                item['city'] = 'all' if exact_location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != exact_location.lower()\
                                        else exact_location.title()
                item['remote'] = job_type
                item['logo_company'] = 'https://www.globant.com/themes/custom/globant_corp_theme/images/2019/globant-logo-dark.svg'
                yield item
