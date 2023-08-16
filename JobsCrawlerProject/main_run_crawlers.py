#
#
#
#
#
import os
import subprocess


# exclude files
exclude = ['__init__.py',]

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'JobsCrawlerProject', 'spiders')

for crawl in os.listdir(path):
    if crawl.endswith('.py') and crawl not in exclude:
        crawler_name = crawl.split('.')[0]
        action = subprocess.run(['scrapy', 'crawl', crawler_name], capture_output=True)
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + crawl)
            print(errors)
        else:
            print("Success crawled " + crawl)
