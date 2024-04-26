import requests  # used to send HTTP requests
from bs4 import BeautifulSoup  # used to parse HTML content
from urllib.parse import urlparse  # used to extract domain from URL
import time  # used to add a delay between requests
import logging  # used to log events to log file
import json  # used to save data in JSON format


logging.basicConfig(filename='url_checker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_existing_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data


def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

        
def get_existing_urls(existing_data):
    return {item['url'] for item in existing_data}


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
        if "Failed to resolve" in str(exception):
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            error_message = f"{url} - Error: The domain '{domain}' does not exist."
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
        # time.sleep(1)
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


def process_links(links, existing_urls, headers):
    url_data = []
    for link in links:
        url = link['href']
        if url in existing_urls:
            continue
        status_code = check_url_redirection(url, headers)
        if status_code is None:
            continue
        url_data.append({'url': url, 'status_code': status_code})
        existing_urls.add(url)
    return url_data


def main():
    url = 'http://127.0.0.1:5500/index.html'
    # url = 'https://github.com/public-api-lists/public-api-lists'
    headers = {
        'User-Agent': 'Sook/1.0/Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }
    json_filename = 'url_data.json'
    
    existing_data = load_existing_data(json_filename)
    existing_urls = get_existing_urls(existing_data)
    
    links = get_links_from_url(url)
    url_data = process_links(links, existing_urls, headers)
    
    updated_data = existing_data + url_data
    save_to_json(updated_data, json_filename)
    
if __name__ == '__main__':
    main()