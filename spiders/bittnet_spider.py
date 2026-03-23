import os
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

os.environ["SCRAPY_SETTINGS_MODULE"] = "JobsCrawlerProject.settings"

current_dir = Path(__file__).resolve().parent
project_dir = current_dir.parent / "JobsCrawlerProject"

sys.path.append(str(project_dir))

from JobsCrawlerProject.spiders.bittnet_spider import BittnetSpiderSpider


def build_settings():
    settings = Settings()
    settings.setmodule("JobsCrawlerProject.settings", priority="project")
    settings.set("SPIDER_MODULES", [], priority="project")
    settings.set("NEWSPIDER_MODULE", "", priority="project")
    settings.set("ITEM_PIPELINES", {}, priority="project")
    settings.set("CONCURRENT_REQUESTS_PER_IP", 0, priority="project")
    settings.set(
        "PLAYWRIGHT_CONTEXTS",
        {"default": {"ignore_https_errors": True}},
        priority="project",
    )
    return settings


if __name__ == "__main__":
    process = CrawlerProcess(build_settings())
    process.crawl(BittnetSpiderSpider)
    process.start()
