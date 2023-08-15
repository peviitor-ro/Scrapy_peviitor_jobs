#
#
#
#
#
from .update_peviitor_api import UpdateAPI


class UpdateAPIPipeline:

    def open_spider(self, spider):
        self.api_updater = UpdateAPI()
        self.lst = []
        self.logo_company = None

    def process_item(self, item, spider):
        data = {
            "id": item.get("id"),
            "job_title": item["job_title"],
            "job_link": item["job_link"],
            "country": item["country"],
            "company": item["company"],
            "city": item["city"],
            }

        self.logo_company = item['logo_company']
        #
        self.lst.append(data)

        return item

    def close_spider(self, spider):

        if self.lst:
            self.api_updater.update_data(self.lst[0]["company"], self.lst)
            #
            self.api_updater.update_logo(self.lst[0]["company"], self.logo_company)
