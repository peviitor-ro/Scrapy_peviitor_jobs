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

    def process_item(self, item, spider):
        data = {
            "job_title": item.get("job_title"),
            "job_link": item.get("job_link"),
            "country": item.get("country"),
            "county": item.get('county'),
            "company": item.get("company"),
            "city": item.get("city"),
            "remote": item.get('remote')
            }

        #
        self.lst.append(data)

        return item

    def close_spider(self, spider):
        if self.lst:
            company = self.lst[0]["company"] if self.lst else "unknown"
            self.api_updater.update_jobs(company, self.lst)
