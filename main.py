import os

from utils.data_handler import load_existing_data
from utils.link_extractor import get_links_from_url
from utils.url_checker import process_links

def main():
    # url = 'https://github.com/public-api-lists/public-api-lists'
    url = 'http://127.0.0.1:5500/'
    headers = {
        'User-Agent': 'Sook/1.0 (mailto:your.email@example.com) Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    
    json_filename = os.path.join('data', 'url_data.json')
    existing_urls = load_existing_data(json_filename)
    links = get_links_from_url(url)
    process_links(links, existing_urls, headers, json_filename)

if __name__ == '__main__':
    main()
