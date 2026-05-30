import scrapy
from JobsCrawlerProject.items import JobItem
from JobsCrawlerProject.found_county import get_county


class RowebSpiderSpider(scrapy.Spider):
    name = "roweb_spider"
    allowed_domains = ["www.roweb.ro"]
    start_urls = ["https://www.roweb.ro/careers"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        for job in response.xpath('//div[@class="content-wrapper"]'):

            link = job.xpath('.//a[@class="sg-jobs-card-button"]/@href').extract_first()
            if not link:
                continue

            location_text = job.xpath('.//p/text()').extract_first()
            location_text = location_text.strip() if location_text else ''

            cities = []
            remote_types = []

            if location_text:
                text_lower = location_text.lower()

                if 'remote' in text_lower:
                    remote_types.append('remote')
                if 'hybrid' in text_lower:
                    remote_types.append('hybrid')

                if ' or ' in text_lower:
                    city_part = location_text.split(' or ')[0].strip()
                else:
                    city_part = location_text

                for kw in ('Remote', 'remote', 'Hybrid', 'hybrid'):
                    city_part = city_part.replace(kw, '')

                raw_cities = [c.strip() for c in city_part.split(',') if c.strip()]
                for c in raw_cities:
                    cities.append('Bucuresti' if c.lower() == 'bucharest' else c)
            else:
                cities = ['Pitesti', 'Bucuresti', 'Craiova']

            if not remote_types:
                remote_types.append('on-site')

            county_list = []
            city_list = []
            for c in cities:
                county_result = get_county(location=c)
                if True in county_result:
                    county_list.append(county_result[0])
                    if c.lower() == county_result[0].lower() and 'bucuresti' not in c.lower():
                        city_list.append('all')
                    else:
                        city_list.append(c)
                else:
                    county_list.append('')
                    city_list.append(c)

            county = county_list if len(county_list) > 1 else (county_list[0] if county_list else '')
            city = city_list if len(city_list) > 1 else (city_list[0] if city_list else '')

            item = JobItem()
            item['job_link'] = 'https://www.roweb.ro/' + link
            item['job_title'] = job.xpath('.//h3/text()').extract_first()
            item['company'] = 'Roweb'
            item['country'] = 'Romania'
            item['county'] = county
            item['city'] = city
            item['remote'] = remote_types
            item['logo_company'] = 'https://interfoane.ro/wp-content/uploads/2016/11/roweb.jpg'

            yield item
