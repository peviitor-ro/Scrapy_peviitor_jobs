#
#
#
#
# Company - PlaySolutions
# Link ----> https://play-solutions.ro/cariere/
#
import scrapy
from JobsCrawlerProject.items import JobItem
from scrapy.selector import Selector
#
from JobsCrawlerProject.found_county import (
    get_county, 
    counties,
    remove_diacritics,
)
from urllib.parse import urlencode
#
import re


class PlaySolutionsSpider(scrapy.Spider):
    name = "play_solutions"
    allowed_domains = ["play-solutions.ro"]
    start_urls = ["https://play-solutions.ro/cariere/"]

    def start_requests(self):
        headers = {
            'authority': 'play-solutions.ro',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://play-solutions.ro',
            'referer': 'https://play-solutions.ro/en_en/cariere-play/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'action': 'jet_smart_filters',
            'provider': 'jet-engine/default',
            'defaults[post_status][]': 'publish',
            'defaults[post_type]': 'cariere',
            'defaults[posts_per_page]': '6',
            'defaults[paged]': '1',
            'defaults[ignore_sticky_posts]': '1',
            'defaults[orderby]': 'modified',
            'settings[lisitng_id]': '1896',
            'settings[columns]': '1',
            'settings[columns_tablet]': '',
            'settings[columns_mobile]': '',
            'settings[column_min_width]': '240',
            'settings[column_min_width_tablet]': '',
            'settings[column_min_width_mobile]': '',
            'settings[inline_columns_css]': 'false',
            'settings[post_status][]': 'publish',
            'settings[use_random_posts_num]': '',
            'settings[posts_num]': '6',
            'settings[max_posts_num]': '9',
            'settings[not_found_message]': 'No data was found',
            'settings[is_masonry]': '',
            'settings[equal_columns_height]': '',
            'settings[use_load_more]': '',
            'settings[load_more_id]': '',
            'settings[load_more_type]': 'click',
            'settings[load_more_offset][unit]': 'px',
            'settings[load_more_offset][size]': '0',
            'settings[loader_text]': '',
            'settings[loader_spinner]': '',
            'settings[use_custom_post_types]': '',
            'settings[custom_post_types]': '',
            'settings[hide_widget_if]': '',
            'settings[carousel_enabled]': '',
            'settings[slides_to_scroll]': '1',
            'settings[arrows]': 'true',
            'settings[arrow_icon]': 'fa fa-angle-left',
            'settings[dots]': '',
            'settings[autoplay]': 'true',
            'settings[pause_on_hover]': 'true',
            'settings[autoplay_speed]': '5000',
            'settings[infinite]': 'true',
            'settings[center_mode]': '',
            'settings[effect]': 'slide',
            'settings[speed]': '500',
            'settings[inject_alternative_items]': '',
            'settings[scroll_slider_enabled]': '',
            'settings[scroll_slider_on][]': [
                'desktop',
                'tablet',
                'mobile',
            ],
            'settings[custom_query]': '',
            'settings[custom_query_id]': '',
            'settings[_element_id]': '',
            'props[found_posts]': '7',
            'props[max_num_pages]': '2',
            'props[page]': '1',
            'paged': None,
            'indexing_filters': '[1943,1962,1966,2032,2005]',
        }

        page = 1
        while True:
            data['paged'] = str(page)
            yield scrapy.Request(
                url='https://play-solutions.ro/wp-admin/admin-ajax.php',
                callback=self.parse_job,
                headers=headers,
                body=urlencode(data).encode('utf-8'),
                method='POST'
            )

            page += 1

    def parse_job(self, response):
        
        if len(res := Selector(text=response.json().get('content')).xpath('//div[contains(@class,\
                                                    "elementor-container")]')) > 0:
            for job in res:  
                location = remove_diacritics(job.xpath('.//h2[contains(@class, "elementor-heading-title")\
                                     and contains(@class, "elementor-size-default")]//text()').extract()[-1].lower())
                
                city, county, job_type = list(), list(), None
                if 'remote' in location:
                    city, county, job_type = None, None, 'remote'
                else:
                    job_type = 'on-site'
                
                # logic for extracting multiple locations from string
                if 'remote' not in location and 'hybrid' not in location:
                    for search_city in counties:
                        for k, v in search_city.items():

                            # add county to locations list
                            if k not in v:
                                v.append(k)

                            for ccity in v:
                                if re.search(r'\b{}\b'.format(re.escape(ccity.lower())), location):
                                    city.append(ccity)
                                elif re.search(r'\bbucharest\b'.format(re.escape(ccity.lower())), location):
                                    city.append('Bucuresti')

                # trebuie sa fac set din lista de orase, ca sunt duplicate.
                location_finish = None
                if city is not None:
                    location_finish = [get_county(location=local_location) for local_location in list(set(city))]

                for_counties = '' if location_finish == None else [x[0] for x in location_finish]
                for_locations = '' if location_finish == None else ['all' if xx[0].lower() == location_finish[i][0].lower()\
                                    and True in location_finish[i] and 'bucuresti' != xx[0].lower()\
                                        else xx[0] for i, xx in enumerate(location_finish)]
                
                print(for_counties)

                #
                item = JobItem()
                item['job_link'] = job.xpath('.//a[@class="jet-listing-dynamic-link__link"]/@href').extract_first()
                item['job_title'] = job.xpath('.//span[@class="jet-listing-dynamic-link__label"]//text()').extract_first()
                item['company'] = 'PlaySolutions'
                item['country'] = 'Romania'
                item['county'] = '' if location_finish == None else for_counties
                item['city'] = '' if for_locations is None else 'all' if 'all' in for_locations else for_locations
                item['remote'] = job_type
                item['logo_company'] = 'https://play-solutions.ro/wp-content/uploads/2021/05/logo_play_header_blue.svg'
                yield item

        else:
            self.crawler.engine.close_spider(self, 'No valid data found')
       
