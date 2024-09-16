#
#
#
#
# Company -> Testronic
# Link ----> https://apply.workable.com/testronic/#jobs
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county
#
import json
class TestronicSpiderSpider(scrapy.Spider):
    name = "testronic_spider"
    allowed_domains = ["apply.workable.com"]
    start_urls = ["https://apply.workable.com/testronic/#jobs"]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],
                             method='HEAD',
                             callback=self.parse_headers)


    def parse_headers(self, response):
        # try to return fresh cookies ids:
        wmc = None
        cf_bm = None
        if (response_headers := {key.decode('utf-8'): [value.decode('utf-8')\
                                     for value in values] for key, values\
                                        in response.headers.items()}):
            
            for key, value in response_headers.items():
                for data in value:
                    for fresh_cookie in data.split():
                        if "wmc" in fresh_cookie:
                            wmc = fresh_cookie
                        elif "__cf_bm" in fresh_cookie:
                            cf_bm = fresh_cookie

       
        formdata = {
                "query": "",
                "department": [],
                "location": [
                    {
                    "country": "Romania",
                    "region": "Bucharest",
                    "city": "Bucharest",
                    "countryCode": "RO"
                    }
                ],
                "remote": [],
                "workplace": [],
                "worktype": []
                }
        headers = {
                'authority': 'apply.workable.com',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'cookie': ' '.join(filter(None, [wmc.split()[0] if wmc else None,cf_bm.split()[0] if cf_bm else None])),
                'origin': 'https://apply.workable.com',
                'referer': 'https://apply.workable.com/testronic/',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
            }

        yield scrapy.Request(
            url='https://apply.workable.com/api/v3/accounts/testronic/jobs',
            method='POST',
            headers=headers,
            body=json.dumps(formdata),
            callback=self.parse
        )


    def parse(self, response):
        data = json.loads(response.text)
        jobs = data.get("results", [])

        for job in jobs:
            location = 'Bucuresti' if job['location']['city'].lower() == 'bucharest' else job['location']['city']
            location_finish = get_county(location=location)

            item = JobItem()
            item['job_link'] = f"https://apply.workable.com/testronic/j/{job['shortcode']}/"
            item['job_title'] = job.get('title')
            item['company'] = "Testronic"
            item['country'] = job['location']['country']
            item['county'] = location_finish[0] if True in location_finish else None
            item['city'] = 'all' if location.lower() == location_finish[0].lower()\
                            and True in location_finish and 'bucuresti' != location.lower()\
                                else location
            item['remote'] = 'remote' if job.get('remote') else 'on-site',
            item['logo_company'] = 'https://workablehr.s3.amazonaws.com/uploads/account/open_graph_logo/585016/social?1695854796000'
            yield item
            