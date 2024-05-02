import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import logging
import json

logging.basicConfig(filename='url_checker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_existing_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return {item['url'] for item in data}
    except FileNotFoundError:
        return set()

def append_to_json(data, filename):
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)

def get_links_from_url(url):
    logging.info(f"Retrieving links from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=lambda href: href and href.startswith('https://'))
    logging.info(f"Found {len(links)} links")
    return links

def log_url_status(url, status_code):
    message = f"{status_code} - {url}"
    print(message)
    logging.info(message)

def handle_request_exception(url, exception):
    if isinstance(exception, requests.exceptions.Timeout):
        error_message = f"{url} - Error: Request timed out."
    elif isinstance(exception, requests.exceptions.ConnectionError):
        error_message = f"{url} - Error: Connection error occurred."
    elif isinstance(exception, requests.exceptions.HTTPError):
        error_message = f"{url} - Error: HTTP error occurred - {str(exception)}"
    else:
        error_message = f"{url} - {str(exception)}"
    print(error_message)
    logging.error(error_message)

def handle_general_exception(url, exception):
    error_message = f"{url} - Error: An unexpected error occurred - {str(exception)}"
    print(error_message)
    logging.error(error_message)

def check_url_redirection(url, headers):
    try:
        logging.info(f"Checking redirection for: {url}")
        response = requests.head(url, allow_redirects=True, headers=headers)
        status_code = response.status_code
        log_url_status(url, status_code)
        return status_code
    except requests.exceptions.RequestException as e:
        handle_request_exception(url, e)
    except Exception as e:
        handle_general_exception(url, e)
    return None

def process_links(links, existing_urls, headers, json_filename):
    for link in links:
        url = link['href']
        if url in existing_urls:
            continue

        status_code = check_url_redirection(url, headers)
        if status_code is None:
            continue

        url_data = {'url': url, 'status_code': status_code}
        append_to_json(url_data, json_filename)
        existing_urls.add(url)

def main():
    url = 'https://github.com/public-api-lists/public-api-lists'
    headers = {
        'User-Agent': 'Sook/1.0 (mailto:your.email@example.com) Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    json_filename = 'url_data.json'
    existing_urls = load_existing_data(json_filename)
    links = get_links_from_url(url)
    process_links(links, existing_urls, headers, json_filename)
    
if __name__ == '__main__':
    main()
