# 


from typing import Iterable
import scrapy


class KassalSpiderSpider(scrapy.Spider):
    name = "kassal_spider"
    allowed_domains = ["kassal.app"]
    start_urls = ["https://kassal.app/api"]

    def start_requests(self):
        headers = {
                'content-type': 'application/json',
                'Authorization': 'Bearer DjXa4OnZKj5Cyhxh0q4RwpNiIKGI59Swao2cGHI5',
            }
        
        page = 1
        while True:
            yield scrapy.Request(
                url=f'https://kassal.app/api/v1/products?page={str(page)}',
                method='GET',
                headers=headers,
            )

            page += 1

            if page == 3:
                # close test spider
                self.crawler.engine.close_spider(self, 'No valid data found')

    def parse(self, response):
        
        if len(data_json := response.json().get('data')) > 0:
            for dat in data_json:
                yield {
                    'gtin': dat.get('ean'),
                    'article_name': dat.get('name'),
                    'brand': dat.get('brand'),
                    'categories': [x.get('name') for x in dat.get('category')],
                    'retailer': dat.get('store').get('name')
                }
        
        # close spider
        else:
            self.crawler.engine.close_spider(self, 'No valid data found')

            print('--------------------------------')


