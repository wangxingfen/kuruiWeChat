import requests
from bs4 import BeautifulSoup
import time
import re

def advanced_crawler(url, keywords, max_depth=3):
    def crawl(current_url, depth):
        if depth > max_depth:
            return
        
        try:
            response = requests.get(current_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', href):
                    if href not in visited_links:
                        visited_links.add(href)
                        if any(keyword in href for keyword in keywords):
                            print(f"Found keyword in URL: {href}")
                            crawl(href, depth + 1)
            
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    
    visited_links = set()
    crawl(url, 1)

start_url = 'https://news.baidu.com/'
search_keywords = ['china', 'us', 'uk']
advanced_crawler(start_url, search_keywords)
