#
#
#
#
#
import scrapy


class JobItem(scrapy.Item):
    id = scrapy.Field()
    job_title = scrapy.Field()
    job_link = scrapy.Field()
    company = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    logo_company = scrapy.Field()
