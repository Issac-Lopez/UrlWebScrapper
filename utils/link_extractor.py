import requests
from bs4 import BeautifulSoup
import logging

def get_links_from_url(url):
    logging.info(f"Retrieving links from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=lambda href: href and href.startswith('https://'))
    logging.info(f"Found {len(links)} links")
    return links