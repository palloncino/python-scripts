import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import json

class ApspSpider(scrapy.Spider):
    name = 'apsp'
    allowed_domains = ['apspstrigno.it']
    start_urls = ['http://www.apspstrigno.it/']

    custom_settings = {
        'DOWNLOAD_DELAY': 3.5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'RETRY_TIMES': 5,
        'ROBOTSTXT_OBEY': True,
        'JOBDIR': 'crawls/apsp'  # Enables auto-resume feature
    }

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.outcome_file_path = './outcome.json'
        self.visited_urls = self.load_visited_urls()

    def parse(self, response):
        if response.url in self.visited_urls:
            return  # Skip the page if it has already been visited
        
        self.driver.get(response.url)
        time.sleep(3.5)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        page_data = {'url': response.url, 'page_links': [], 'file_links': []}

        for link in soup.find_all('a', href=True):
            url = link['href']
            if url.startswith(self.start_urls[0]):
                if self.is_file_link(url):
                    page_data['file_links'].append(url)
                elif self.is_page_link(url):
                    page_data['page_links'].append(url)
                    if url not in self.visited_urls:
                        yield response.follow(url, self.parse)
        
        self.visited_urls.add(response.url)
        self.append_data(page_data)

    def append_data(self, data):
        with open(self.outcome_file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')

    def load_visited_urls(self):
        try:
            with open(self.outcome_file_path, 'r') as f:
                return {json.loads(line)['url'] for line in f}
        except FileNotFoundError:
            return set()

    def is_file_link(self, url):
        return bool(re.search(r'/.+/.+', url)) and not self.is_page_link(url)

    def is_page_link(self, url):
        return bool(re.search(r'/\d+(-\d+)*$', url))

    def closed(self, reason):
        self.driver.quit()

# Running the spider with the JOBDIR setting for auto-resume
process = CrawlerProcess()
process.crawl(ApspSpider)
process.start()
