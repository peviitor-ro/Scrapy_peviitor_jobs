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
            "job_title": item.get("job_title"),
            "job_link": item.get("job_link"],
            "country": item.get("country"),
            "county": item.get('county'),
            "company": item.get("company"),
            "city": item.get("city"),
            "remote": item.get('remote')
            }
        
        self.logo_company = item.get('logo_company')
        #
        self.lst.append(data)

        return item

    def close_spider(self, spider):

        if self.lst:
            self.api_updater.update_data(self.lst[0]["company"], self.lst)
            #
            self.api_updater.update_logo(self.lst[0]["company"], self.logo_company)

        else:
            self.api_updater.only_clean_data(self.lst[0]["company"])
