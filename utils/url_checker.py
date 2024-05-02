import requests
import logging

from utils.data_handler import append_to_json

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