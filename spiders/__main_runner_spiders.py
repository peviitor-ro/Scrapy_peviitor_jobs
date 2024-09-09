import os
import subprocess

# exclude files
exclude = ['__init__.py',
           '__main_runner_spiders.py',
           'tesla_spider.py',
           'rscrds_spider.py',
           'globant_spider.py',
           'bittnet_spider.py',
           ]

path = os.path.dirname(os.path.abspath(__file__))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        action = subprocess.run(['python', os.path.join(path, site)], capture_output=True)
        if action.returncode != 0:
            errors = action.stderr.decode('utf-8')
            print("Error in " + site)
            print(errors)
        else:
            print("Success scraping " + site)
