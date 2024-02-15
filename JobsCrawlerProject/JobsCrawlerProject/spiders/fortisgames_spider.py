#
#
#
#
# Company -> FORTISGames
# Link ----> https://fortisgames.com/careers/#open-positions
#
import scrapy
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


# func for save data to dict()
# expect DRY
def return_lst_dict(title: str, link: str, loc: str) -> dict:
    '''
    ... this function will return a dict to append to a list and avoid DRY
    '''
    dct = {
                "job_title": title,
                "job_link": link,
                "company": "FORTISGames",
                "country": "Romania",
                "city": loc
            }

    return dct


class FortisgamesSpiderSpider(scrapy.Spider):
    name = "fortisgames_spider"
    allowed_domains = ["fortisgames.com"]
    start_urls = ["https://boards-api.greenhouse.io/v1/boards/fortisgames/departments?render_as=tree"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):

        # general dict with data for items()
        # no DRY
        lst_with_data = []  # store dicts here
        for job in response.json().get("departments"):

            # first next for!
            for job_job in job.get("children"):
                if len(job_job.get("jobs")) > 0:
                    for j1_job in job_job.get("jobs"):
                        loco = j1_job.get("location").get("name")

                        if 'romania' in loco.lower():
                            lst_with_data.append(return_lst_dict(
                                                 title=j1_job.get("title"),
                                                 link=j1_job.get("absolute_url"),
                                                 loc=loco))

            # second for ---> jobs
            if len(job.get("jobs")) > 0:
                for job_2 in job.get("jobs"):
                    loco = j1_job.get("location").get("name")

                    if 'romania' in loco.lower():
                        lst_with_data.append(return_lst_dict(
                                             title=j1_job.get("title"),
                                             link=j1_job.get("absolute_url"),
                                             loc=loco))

        for ddict in lst_with_data:

            loca = ddict.get('city').lower()
            
            item = JobItem()
            item['job_link'] = ddict.get('job_link')
            item['job_title'] = ddict.get('job_title')
            item['company'] = ddict.get('company')
            item['country'] = ddict.get('country')
            item['county'] = '' if 'remote' in loca else get_county(loca.split('-')[0].title())
            item['city'] = '' if 'remote' in loca else loca.split('-')[0].title()
            item['remote'] = 'remote' if 'remote' in loca else 'on-site'
            item['logo_company'] = 'https://media.pocketgamer.biz/2022/3/115185/fortis-r225x225.jpg'
            yield item
