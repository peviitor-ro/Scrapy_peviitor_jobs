#
#
#
#
#
from typing import Union
from scrapy import Item, Field


class JobItem(Item):
    job_title:      str                 = Field()
    job_link:       str                 = Field()
    company:        str                 = Field()
    country:        str                 = Field()
    county:         Union[str, list]    = Field()
    city:           Union[str, list]    = Field()
    remote:         str                 = Field()
    logo_company:   str                 = Field()
