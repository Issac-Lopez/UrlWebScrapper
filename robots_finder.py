import requests

def get_robots_txt(url):
    robots_url = f"{url}/robots.txt"
    
    try:
        response = requests.get(robots_url)
        
        if response.status_code == 200:
            print(f"Robots.txt found for {url}")
            print("Content of robots.txt:")
            print(response.text)
        else:
            print(f"No robots.txt found for {url}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while retrieving robots.txt for {url}: {str(e)}")

# Example usage
website_url = "https://www.github.com"
get_robots_txt(website_url)