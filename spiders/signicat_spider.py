import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

os.environ['SCRAPY_SETTINGS_MODULE'] = 'JobsCrawlerProject.settings'

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', 'JobsCrawlerProject'))

sys.path.append(project_dir)

from JobsCrawlerProject.spiders.signicat_spider import SignicatSpiderSpider

if __name__ == "__main__":
    # Initialize the crawling process with the project's settings
    process = CrawlerProcess(get_project_settings())
    process.crawl(SignicatSpiderSpider)
    process.start()
