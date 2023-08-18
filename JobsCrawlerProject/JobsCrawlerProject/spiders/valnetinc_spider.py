#
#
#
#
# Company -> ValnetInc
# Link ----> https://valnetinc.applytojob.com/apply
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class ValnetincSpiderSpider(scrapy.Spider):
    name = "valnetinc_spider"
    allowed_domains = ["valnetinc.applytojob.com"]
    start_urls = ["https://valnetinc.applytojob.com/apply"]

    custom_settings = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }

    def start_requests(self):
        yield scrapy.Request("https://valnetinc.applytojob.com/apply")

    def parse(self, response):

        # data here
        for job in response.css('li.list-group-item'):

            # get location
            city = job.css('ul.list-inline.list-group-item-text> li::text').get().strip()

            # check for Romania location
            if 'remote' in city.lower():
                item = JobItem()
                item['id'] = str(uuid.uuid4())
                item['job_link'] = job.css('a::attr(href)').get()
                item['job_title'] = job.css('a::text').get().strip()
                item['company'] = 'ValnetInc'
                item['country'] = 'Romania'
                item['city'] = 'Remote'
                item['logo_company'] = 'https://s3.amazonaws.com/resumator/customer_20170725184012_BUKJMMB5MHBOK8RK/logos/20170726201646_logo_copy.gif'
                #
                yield item
