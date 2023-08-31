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
import uuid


# func for save data to dict()
# expect DRY
def return_lst_dict(title: str, link: str, loc: str) -> dict:
    '''
    ... this function will return a dict to append to a list and avoid DRY
    '''
    dct = {
                "id": str(uuid.uuid4()),
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
        for job in response.json()["departments"]:

            # first next for!
            for job_job in job["children"]:
                if len(job_job["jobs"]) > 0:
                    for j1_job in job_job["jobs"]:
                        loco = j1_job["location"]["name"].split('-')[-1]

                        if 'romania' in loco.lower():
                            lst_with_data.append(return_lst_dict(
                                                 title=j1_job["title"],
                                                 link=j1_job["absolute_url"],
                                                 loc=loco))

            # second for ---> jobs
            if len(job["jobs"]) > 0:
                for job_2 in job["jobs"]:
                    loco = j1_job["location"]["name"].split('-')[-1]

                    if 'romania' in loco.lower():
                        lst_with_data.append(return_lst_dict(
                                             title=j1_job["title"],
                                             link=j1_job["absolute_url"],
                                             loc=loco))

        for ddict in lst_with_data:
            item = JobItem()
            item['id'] = ddict["id"]
            item['job_link'] = ddict['job_link']
            item['job_title'] = ddict['job_title']
            item['company'] = ddict['company']
            item['country'] = ddict['country']
            item['city'] = ddict['city']
            item['logo_company'] = 'https://media.pocketgamer.biz/2022/3/115185/fortis-r225x225.jpg'
            yield item
