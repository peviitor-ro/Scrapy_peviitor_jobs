#
#
#
#
# SEND DATA TO API SCRIPT!
#
#
import requests
#
import os  # I do not have API KEY
#
import json


class UpdateAPI:
    '''
    class for update API
    '''

    def update_data(self, company_name: str, data_jobs: list):
        '''
        ... update data on peviitor.
        '''

        API_KEY = os.environ.get('API_KEY')
        CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

        # clean headers
        clean_header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'apikey': API_KEY
                }

        # clean data
        clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': company_name})

        # post headers
        post_header = {
            'Content-Type': 'application/json',
            'apikey': API_KEY
            }

        # update data
        post_request_to_server = requests.post('https://api.peviitor.ro/v4/update/', headers=post_header, data=json.dumps(data_jobs))

        # don't delete this lines if you want to see the graph on scraper's page
        file = company_name.lower() + '_spider.py'
        data = {'data': len(data_jobs)}
        dataset_url = f'https://dev.laurentiumarian.ro/dataset/Scrapy_peviitor_jobs/{file}/'
        requests.post(dataset_url, json=data)
        # ########################################################

        print(json.dumps(data_jobs, indent=4))

    # only clean data from API
    def only_clean_data(self, company_name: str) -> None:

        API_KEY = os.environ.get("API_KEY")
        CLEAN_URL = "https://api.peviitor.ro/v4/clean/"

        clean_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "apikey": API_KEY
            }

        clean_request = requests.post(url=CLEAN_URL, headers=clean_header, data={"company": company_name})

    # update logo or add logo
    def update_logo(self, id_company: str, logo_link: str):
        '''
        ... update logo on pe viitor.
        '''

        headers = {
            "Content-Type": "application/json"
        }

        url = "https://api.peviitor.ro/v1/logo/add/"
        data = json.dumps([{"id": id_company, "logo": logo_link}])

        response = requests.post(url, headers=headers, data=data)
