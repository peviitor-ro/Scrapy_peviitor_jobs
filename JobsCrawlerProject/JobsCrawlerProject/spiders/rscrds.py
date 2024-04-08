#
#
#
#
#
#
#
# Company -> Roweb
# Link ----> https://www.roweb.ro/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county
#
from urllib.parse import urlencode
import re

from time import sleep


def make_headers(town: str, industry: str) -> tuple[dict, dict]:
    '''
        ---> Make headers for post Request.

        params: Town: str, for search jobs in each town.
                Industry: Exact title job.
        
        return: headers - dict
                payload - dict
    '''
    headers = {
        'authority': 'www.digi.ro',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.digi.ro',
        'referer': 'https://www.digi.ro/cariere',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'assistanceSupportCareers',
        'company': 'rcs-rds',
        'county': f"{town}",
        'industry': f"{industry}",
    }

    return headers, data


class RscrdsSpider(scrapy.Spider):
    name = "rscrds"
    allowed_domains = ["www.digi.ro"]
    start_urls = ["https://www.digi.ro/cariere"]

    def start_requests(self):
        yield scrapy.Request(url='https://www.digi.ro/cariere',
                                    callback=self.parse_towns)
    
    def parse_towns(self, response):
        
        # get all counties
        for city_ro in response.xpath('//select[@id="form-assistance-support-careers-county"]//option'):
            if (location := city_ro.xpath('.//text()').extract_first()) and location.lower() == 'judet':
                continue

            # go through jobs titles
            for job_ro in response.xpath('.//following-sibling::select[@id="form-assistance-support-careers-industry"]//option'):
                if (industry_ro := job_ro.xpath('.//text()').extract_first().strip()) == 'Domenii':
                    continue

                headers, formdata = make_headers(town=location,
                                            industry=industry_ro)

                # send town in next function
                meta = {'location': location}

                yield scrapy.Request(
                        url="https://www.digi.ro/cariere/search-xhr",
                        method="POST",
                        headers=headers,
                        body=urlencode(formdata).encode('utf-8'),
                        callback=self.parse_job,
                        meta=meta,
                    )

    def parse_job(self, response):

        data_response = str(response.text)
        titles = re.findall(r'<label class="accordion-title"[^>]*>([^<]+)<', data_response)
        links = re.findall(r'<a\s+href="([^"]+)"\s+class="btn-round-right"', data_response)

        for idx in range(len(titles)):
            #
            location = response.meta.get('location')
            location_finish = get_county(location=location)
            
            # send data to Pipelines 
            item = JobItem()
            item['job_link'] = f"https://www.digi.ro/{links[idx]}"
            item['job_title'] = titles[idx]
            item['company'] = 'RCS-RDS'
            item['country'] = 'Romania'
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                                    and True in location_finish and 'bucuresti' != location.lower()\
                                        else location
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://www.digi.ro/static/theme-ui-frontend/bin/images/logo-digi-alt.png'
            #
            yield item
