#
#
#
#
# Company -> Upscale
# Link ----> https://upscale.ai/careers
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
import uuid


class UpscaleSpiderSpider(scrapy.Spider):
    name = "upscale_spider"
    allowed_domains = ["devwordpress.upscale.ai"]
    start_urls = ["https://devwordpress.upscale.ai/wp-json/wp/v2/career?&meta=true&order=desc&order_by=date&status=publish"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        #
        for job in response.json():
            item = JobItem()
            item['id'] = str(uuid.uuid4())
            item['job_link'] = f"https://upscale.ai/careers/{job['link'].split('/')[-2]}"
            item['job_title'] = job['title']['rendered']
            item['company'] = 'Upscale'
            item['country'] = 'Romania'
            item['city'] = 'Remote'
            item['logo_company'] = 'https://upscale.ai/images/common/svg/upscaleLogo.svg'
            #
            yield item

curl 'https://devwordpress.upscale.ai/wp-json/wp/v2/career?&meta=true&order=desc&order_by=date&status=publish' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'origin: https://upscale.ai' \
  -H 'referer: https://upscale.ai/' \
  -H 'sec-ch-ua: "Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'