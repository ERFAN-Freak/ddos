import requests
from urllib.parse import urlparse
from urllib3.util import connection
from concurrent.futures import ThreadPoolExecutor
import socks  # Import the 'socks' library

def check_site_status(url, headers=None, use_proxy=False):
    if not urlparse(url).scheme:
        url = 'https://' + url

    try:
        if use_proxy:
            # Set up a session with a SOCKS5 proxy for Tor
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://localhost:2080',  # Tor's default SOCKS5 proxy
                'https': 'socks5://localhost:2080'
            }
            response = session.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Successful - Status Code 200")
        elif response.status_code == 404:
            print("Not Found - Status Code 404")
        else:
            print(f"Unexpected Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def check_sites_concurrently(site, num_threads, headers=None, use_proxy=False):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(check_site_status, site, headers, use_proxy)

if __name__ == "__main__":
    site = input("Enter the site URL:\n==> ")
    num_threads = input("Enter the number of threads to use:\n==> ")

    try:
        num_threads = int(num_threads)
        if num_threads <= 0:
            raise ValueError("Number of threads must be a positive integer.")
    except ValueError:
        print("Invalid input for the number of threads.")
        exit(1)

    use_proxy = input("Do you want to use a proxy (Tor)? (yes/no):\n==> ").lower() == "yes"

    # Define the User-Agent header to mimic Chrome.
    chrome_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    )

    # Create a headers dictionary with the Chrome User-Agent.
    headers = {
        'User-Agent': chrome_user_agent,
    }

    check_sites_concurrently(site, num_threads, headers, use_proxy)
