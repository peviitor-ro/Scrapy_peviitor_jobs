#
#
#
#
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import json


class SustainalyticsSpider(scrapy.Spider):
    name = "sustainalytics_spider"
    allowed_domains = ["careers.morningstar.com"]
    start_urls = ["https://careers.morningstar.com/sustainalytics/widgets"]

    def start_requests(self):
        payload = json.dumps({
          "lang": "en_us",
          "deviceType": "desktop",
          "country": "us",
          "pageName": "search-results",
          "ddoKey": "refineSearch",
          "sortBy": "",
          "subsearch": "",
          "from": 0,
          "jobs": True,
          "counts": True,
          "all_fields": [
            "category",
            "country",
            "state",
            "city",
            "type",
            "visibilityType",
            "brand"
          ],
          "size": 100,
          "clearAll": False,
          "jdsource": "facets",
          "isSliderEnable": False,
          "pageId": "page138",
          "siteType": "sustainalytics",
          "keywords": "",
          "global": True,
          "selected_fields": {
            "country": [
              "Romania"
            ]
          }
        })

        yield scrapy.Request(
            url=self.start_urls[0],
            method="POST",
            body=payload,
            headers={
                'content-type': 'application/json',
                'referer': 'https://careers.morningstar.com/sustainalytics/us/en/search-results',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            },
            callback=self.parse_api,
        )

    def parse_api(self, response):
        data_json = json.loads(response.text)

        for idx, job in enumerate(data_json.get('refineSearch').get('data').get('jobs')):

            # get items with new locations
            item = JobItem()
            item['job_link'] = job.get('title')
            item['job_title'] = job.get('applyUrl').replace('/apply', '')
            item['company'] = 'Sustainalytics'
            item['country'] = 'Romania'
            item['county'] = job.get('cityState')
            item['city'] = job.get('city')
            item['remote'] = 'on-site'
            item['logo_company'] = ''

            yield item
