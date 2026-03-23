import json
import re

import scrapy

from JobsCrawlerProject.found_county import get_county
from JobsCrawlerProject.items import JobItem


class GlobantSpiderSpider(scrapy.Spider):
    name = "globant_spider"
    allowed_domains = ["career.globant.com"]
    api_url = "https://career.globant.com/api/sap/job-requisition-v1"
    logo_url = "https://www.globant.com/themes/custom/globant_corp_theme/images/2019/globant-logo-dark.svg"

    def start_requests(self):
        yield self.build_api_request(page=1)

    def build_api_request(self, page):
        payload = {
            "page": page,
            "q": "",
            "country": "",
            "deparment": "",
        }
        return scrapy.Request(
            url=self.api_url,
            method="POST",
            body=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            callback=self.parse_jobs,
            cb_kwargs={"page": page},
        )

    def parse_jobs(self, response, page):
        data = json.loads(response.text)

        for job in data.get("jobRequisition", []):
            country = (job.get("country") or "").strip()
            location = (job.get("location") or "").strip()
            external_code = (job.get("externalCode") or "").strip().upper()

            if country.lower() != "romania" and "romania" not in location.lower() and external_code != "RO":
                continue

            job_title = (job.get("jobTitle") or "").strip()
            if not job_title:
                continue

            job_req_id = str(job.get("jobReqId") or "").strip()
            slug = self.slugify(job_title)
            exact_location = self.extract_exact_location(location)
            location_finish = get_county(location=exact_location)

            item = JobItem()
            item["job_link"] = f"https://career.globant.com/job/{slug}/{job_req_id}"
            item["job_title"] = job_title
            item["company"] = "Globant"
            item["country"] = "Romania"
            item["county"] = location_finish[0] if True in location_finish else None
            item["city"] = self.build_city(exact_location, location_finish)
            item["remote"] = self.extract_remote_type(job)
            item["logo_company"] = self.logo_url
            yield item

        if data.get("showMore"):
            yield self.build_api_request(page=page + 1)

    def extract_exact_location(self, location):
        normalized_location = re.sub(r"\s+", " ", location).strip()

        if not normalized_location:
            return "all"

        parts = [part.strip() for part in normalized_location.split(",") if part.strip()]
        if not parts:
            return "all"

        first_part = parts[0].lower()
        if first_part in {"romania", "europa", "europe", "global", "multiple locations"}:
            return "all"

        return parts[0]

    def build_city(self, exact_location, location_finish):
        if exact_location == "all":
            return "all"

        if True in location_finish and exact_location.lower() == location_finish[0].lower() and exact_location.lower() != "bucuresti":
            return "all"

        return exact_location.title()

    def extract_remote_type(self, job):
        description = (job.get("jobDescription") or "").lower()
        location = (job.get("location") or "").lower()

        if "#li-hybrid" in description or "hybrid" in description or "hybrid" in location:
            return "hybrid"
        if "remote" in description or "remote" in location:
            return "remote"
        return "on-site"

    def slugify(self, value):
        slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
        return slug or "globant-job"
