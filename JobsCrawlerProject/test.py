import requests

cookies = {
    'PLAY_SESSION': 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiI4YTI4NDI5OS1hMjkyLTQ1NzYtOGI2OC03NDM4ZmRkNmIzNmEifSwibmJmIjoxNzI3NTExODk0LCJpYXQiOjE3Mjc1MTE4OTR9.9Y3JuIN2ESpRzXbKM8QOIac2-pOpC4wOWXnW8M73Oh8',
    'PHPPPE_ACT': '8a284299-a292-4576-8b68-7438fdd6b36a',
    'VISITED_LANG': 'en',
    'VISITED_COUNTRY': 'us',
    'VISITED_VARIANT': 'sustainalytics',
    'PHPPPE_GCC': 'd',
    'ext_trk': 'pjid%3D8a284299-a292-4576-8b68-7438fdd6b36a&p_lang%3Den_us&refNum%3DMORMORUS',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiI4YTI4NDI5OS1hMjkyLTQ1NzYtOGI2OC03NDM4ZmRkNmIzNmEifSwibmJmIjoxNzI3NTExODk0LCJpYXQiOjE3Mjc1MTE4OTR9.9Y3JuIN2ESpRzXbKM8QOIac2-pOpC4wOWXnW8M73Oh8; PHPPPE_ACT=8a284299-a292-4576-8b68-7438fdd6b36a; VISITED_LANG=en; VISITED_COUNTRY=us; VISITED_VARIANT=sustainalytics; PHPPPE_GCC=d; ext_trk=pjid%3D8a284299-a292-4576-8b68-7438fdd6b36a&p_lang%3Den_us&refNum%3DMORMORUS',
    'origin': 'https://careers.morningstar.com',
    'priority': 'u=1, i',
    'referer': 'https://careers.morningstar.com/sustainalytics/us/en/search-results',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-csrf-token': '8ad94d44fcc64ac7ae3899c0a1b8bd34',
}

json_data = {
    'lang': 'en_us',
    'deviceType': 'desktop',
    'country': 'us',
    'pageName': 'search-results',
    'ddoKey': 'refineSearch',
    'sortBy': '',
    'subsearch': '',
    'from': 0,
    'jobs': True,
    'counts': True,
    'all_fields': [
        'category',
        'country',
        'state',
        'city',
        'type',
        'visibilityType',
        'brand',
    ],
    'size': 10,
    'clearAll': False,
    'jdsource': 'facets',
    'isSliderEnable': False,
    'pageId': 'page138',
    'siteType': 'sustainalytics',
    'keywords': '',
    'global': True,
    'selected_fields': {
        'country': [
            'Romania',
        ],
    },
}

response = requests.post(
    'https://careers.morningstar.com/sustainalytics/widgets',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.text)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"lang":"en_us","deviceType":"desktop","country":"us","pageName":"search-results","ddoKey":"refineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","state","city","type","visibilityType","brand"],"size":10,"clearAll":false,"jdsource":"facets","isSliderEnable":false,"pageId":"page138","siteType":"sustainalytics","keywords":"","global":true,"selected_fields":{"country":["Romania"]}}'
#response = requests.post('https://careers.morningstar.com/sustainalytics/widgets', cookies=cookies, headers=headers, data=data)
