import os
import re
import textwrap

# Directory containing the spiders
spiders_dir = os.path.join('JobsCrawlerProject', 'JobsCrawlerProject', 'spiders')

# Directory where the generated scripts will be saved
output_dir = os.path.join('spiders')

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

def find_spiders_in_directory(directory):
    spider_files = []

    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(directory, filename)
            spider_files.append(file_path)

    return spider_files

def extract_spider_class_name(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to find the class extending scrapy.Spider, for various class name styles
    match = re.search(r'class (\w+Spider)\s*\(', content)
    if match:
        return match.group(1)
    return None

def generate_script(file_path, spider_class_name):
    module_name = os.path.basename(file_path)[:-3]  # Remove the .py extension
    script_content = textwrap.dedent(f"""
import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', 'JobsCrawlerProject'))

sys.path.append(project_dir)

from JobsCrawlerProject.spiders.{module_name} import {spider_class_name}

if __name__ == "__main__":
    # Initialize the crawling process with the project's settings
    process = CrawlerProcess(get_project_settings())
    process.crawl({spider_class_name})
    process.start()
""")

    output_file_path = os.path.join(output_dir, f'{module_name}.py')
    with open(output_file_path, 'w') as f:
        f.write(script_content)
    print(f"Generated script: {output_file_path}")

def main():
    spider_files = find_spiders_in_directory(spiders_dir)

    for file_path in spider_files:
        module_name = os.path.basename(file_path)[:-3]  # Remove the .py extension
        spider_class_name = extract_spider_class_name(file_path)
        if spider_class_name:
            generate_script(file_path, spider_class_name)
        else:
            print(f"No spider class found in {file_path}")

if __name__ == "__main__":
    main()
