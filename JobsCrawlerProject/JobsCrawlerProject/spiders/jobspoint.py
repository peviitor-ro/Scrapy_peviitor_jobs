#
#
#
#
#
#
#
import scrapy
from JobsCrawlerProject.items import JobItem


class JobspointSpider(scrapy.Spider):
    name = "jobspoint"
    allowed_domains = ["jobspoint.ro"]
    start_urls = ["https://jobspoint.ro/ro"]

    custom_headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-october-request-handler': 'onFilter',
        'x-requested-with': 'XMLHttpRequest',
    }

    # def start_requests(self):
    #     page = 1
    #     while True:
    #         yield scrapy.FormRequest(
    #             url="https://jobspoint.ro/ro/jobs?homeFilterKeywords=",
    #             method="POST",
    #             headers=self.custom_headers,
    #             formdata={'page': str(page)}
    #             )

    #         page += 1

    # def parse(self, response):
    #     print(response.json().get('#filteredList'))
