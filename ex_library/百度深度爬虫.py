import requests
from bs4 import BeautifulSoup
import time
import random
import os

# 目标网址，这里替换为百度官网
url = 'https://www.taptap.cn/'

# 模拟浏览器头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 发送HTTP请求
def fetch(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return response.text
    except requests.exceptions.HTTPError as e:
        print('HTTP Error:', e)
    except requests.exceptions.RequestException as e:
        print('Error:', e)
    return None

# 解析网页内容
def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    links = [a['href'] for a in soup.find_all('a', href=True)]
    text_content = soup.get_text()
    return title, links, text_content

# 深度爬取函数
def crawl(url, depth=1):
    if depth <= 0:
        return
    
    html = fetch(url)
    if html:
        title, links, text_content = parse(html)
        
        # 将输出结果保存到文件中
        with open('baidu_crawl_results.txt', 'a', encoding='utf-8') as file:
            file.write('Title: {}\n'.format(title.encode('utf-8', errors='ignore').decode('utf-8')))
            file.write('Text Content: {}\n\n'.format(text_content.encode('utf-8', errors='ignore').decode('utf-8')))
        
        for link in links:
            # 构建完整的URL
            full_url = url + link
            time.sleep(random.randint(0.1,0.3 ))
            # 递归调用，实现深度爬取
            crawl(full_url, depth - 1)

# 创建文件以保存结果，如果文件存在则清空内容
if os.path.exists('baidu_crawl_results.txt'):
    os.remove('baidu_crawl_results.txt')

# 开始深度爬取，假设深度为2
crawl(url, depth=2)
