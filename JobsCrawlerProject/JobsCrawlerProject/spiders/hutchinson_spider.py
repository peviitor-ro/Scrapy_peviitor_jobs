#
#
#
# Playwright
# Company -> Hutchinson
# Link ----> https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1007
#
import scrapy
#
from JobsCrawlerProject.items import JobItem
#
from JobsCrawlerProject.found_county import get_county


class HutchinsonSpiderSpider(scrapy.Spider):
    name = "hutchinson_spider"

    allowed_domains = ["fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com"]
    start_urls = ["https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1007/requisitions?location=Romania&locationId=300000000378617&locationLevel=country&mode=location"]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],
                             callback=self.parse_headers,
                             method='HEAD')
        
    def parse_headers(self, response):
        
        # try to return fresh cookies ids:
        ora_fnd = None
        j_session_id = None
        if (response_headers := {key.decode('utf-8'): [value.decode('utf-8')\
                                     for value in values] for key, values\
                                        in response.headers.items()}):
            

            for key, value in response_headers.items():
                for data in value:
                    for fresh_cookie in data.split():
                        if "ORA_FND_SESSION" in fresh_cookie:
                            ora_fnd = fresh_cookie
                        elif "JSESSIONID" in fresh_cookie:
                            j_session_id = fresh_cookie

        url = 'https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_1007,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000000378617,sortBy=POSTING_DATES_DESC'

        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/vnd.oracle.adf.resourceitem+json;charset=utf-8',
            'Cookie': f"{ora_fnd} {j_session_id}",
            'Referer': 'https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1007/requisitions?mode=location',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }


        yield scrapy.Request(
                url=url,
                method='GET',
                headers=headers,
                callback=self.parse_data_from_API,
            )

    def parse_data_from_API(self, response):

        for job in response.json().get('items')[0].get('requisitionList'):

            #
            if (location := job.get('PrimaryLocation').split(',')[0].lower()) == 'romania':
                location = 'all'

            item = JobItem()
            item['job_link'] = f"https://fa-eocc-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1007/job/{job.get('Id')}/?location=Romania&locationId=300000000378617&locationLevel=country&mode=location"
            item['job_title'] = job.get('Title')
            item['company'] = 'Hutchinson'
            item['country'] = 'Romania'
            item['county'] = 'all' if location == 'all' else get_county(location.title())
            item['city'] = location if location == 'all' else location.title()
            item['remote'] = 'on-site'
            item['logo_company'] = 'https://cdn.worldvectorlogo.com/logos/hutchinson-logo.svg'
            #
            yield item