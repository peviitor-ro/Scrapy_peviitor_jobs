import requests

cookies = {
    'ASP.NET_SessionId': '5nsjqzscm3dj5lamwkdtazxk',
    '_ga': 'GA1.1.1505555080.1725686916',
    '_ga_QT732PRYQ5': 'GS1.1.1725686916.1.1.1725687081.0.0.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ASP.NET_SessionId=5nsjqzscm3dj5lamwkdtazxk; _ga=GA1.1.1505555080.1725686916; _ga_QT732PRYQ5=GS1.1.1725686916.1.1.1725687081.0.0.0',
    'origin': 'https://www.bittnet.jobs',
    'priority': 'u=1, i',
    'referer': 'https://www.bittnet.jobs/1048/lista-posturi',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

data = 'transport=fIh90vbStQIALVzhryTM9x36QRnts/ePtYlI87cxS0cXz19ykXlxbmAJ1k7B0ZDAjCVuZLJPXOGvl42IJKBKDFzMDFBnFyczbKnMCBUWY9Y6+PE3vJcHEA4ilpm3RcGcpaJbyMOhThOc2OZxj8WuogjgJZf1glGs07nPpuj04bjgzGFMsx0ZLQ1m4hNV8VckIywX09XfIa8ift0H0nIUF/aMlw6ui9gnTWtfUrZ65Kk=&cykey=yhTnkx4AofxD9K0n1TJYbAEdsWckBfYiiA5mTdn9%2FrZa10omTwwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwZh6CC5IhK18CffRpE6PkfwCCn2q3xlemTWYBmgXvtBQTFCp16Sq1VBf2ZG2%2FPwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwA3zcR7S1AdkOqhPcLZZk%2FijZQCEwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwXu02H2nnZxuBvrZ7XzFOcyeMnpt2kqqtbs%2FwwwwwwwwAAAAAA123456789AAAAAAAAwwwwwwwwmohjcFJw287vSc%2F8HjsEH7jLyHRvRYPVpvYeQ%3D%3D'

response = requests.post('https://www.bittnet.jobs/api/dataexchange', cookies=cookies, headers=headers, data=data)
print(response.text)
