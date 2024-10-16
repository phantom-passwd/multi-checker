from clear import clear
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os, re, requests, ctypes, colorama
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProxyScraper:
    categories = {
        'HTTP': [],
        'HTTPS': [],
        'SOCKS4': [],
        'SOCKS5': []
    }
    total_proxies = 0

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def log(message):
        print(f"{colorama.Fore.LIGHTBLUE_EX}[ {ProxyScraper.get_time()} ] {colorama.Fore.LIGHTBLACK_EX} --->> {colorama.Fore.LIGHTMAGENTA_EX + colorama.Fore.LIGHTCYAN_EX}{message}{colorama.Fore.RESET}")

    proxy_sites = [
        'https://www.freeproxy.world/',
        'https://openproxylist.com/proxy/',
        'https://proxydb.net/',
        "https://proxyscrape.com/free-proxy-list",
        "https://www.sslproxies.org/",
        "https://free-proxy-list.net/",
        "https://www.us-proxy.org/",
        "https://proxy-list.download/HTTP",
        "https://proxy-list.download/HTTPS",
        "https://proxy-list.download/SOCKS4",
        "https://proxy-list.download/SOCKS5",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://spys.me/proxy.txt",
        "https://www.proxyscan.io/download?type=socks5",
        "https://hidemy.name/en/proxy-list/",
        "https://www.my-proxy.com/free-proxy-list.html",
        "https://openproxy.space/list/http",
        "https://openproxy.space/list/socks4",
        "https://openproxy.space/list/socks5",
        'https://raw.githubusercontent.com/clarketm/proxy-list/refs/heads/master/proxy-list.txt',
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://www.socks-proxy.net/"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }

    @staticmethod
    def scrape_sub_links(base_url):
        sub_links = []
        try:
            response = requests.get(base_url, headers=ProxyScraper.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(base_url, href)
                if base_url in full_url:
                    sub_links.append(full_url)
        except requests.RequestException as e:
            ProxyScraper.log(f"Error from {base_url}: {e}")
        return sub_links

    @staticmethod
    def clean_proxies():
        ip_regex = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d{1,5}$'
        )
        for category in ProxyScraper.categories:
            filename = f"{category.lower()}_proxies.txt"
            valid_proxies = []
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    proxies = f.readlines()
                    for proxy in proxies:
                        proxy = proxy.strip()
                        if ip_regex.match(proxy) and all(len(part) >= 2 for part in proxy.split(':')[0].split('.')):
                            valid_proxies.append(proxy)
                with open(filename, 'w') as f:
                    for proxy in valid_proxies:
                        f.write(proxy + '\n')
                ProxyScraper.log(f"Cleaned {len(valid_proxies)} valid {category} proxies in '{filename}'.")

    @staticmethod
    def scrape_proxies():
        futures = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for url in ProxyScraper.proxy_sites:
                all_links = [url] + ProxyScraper.scrape_sub_links(url)
                for link in all_links:
                    futures.append(executor.submit(ProxyScraper.fetch_and_process, link))
            for future in as_completed(futures):
                future.result()
        return ProxyScraper.categories

    @staticmethod
    def fetch_and_process(link):
        try:
            response = requests.get(link, headers=ProxyScraper.headers, timeout=10)
            ProxyScraper.log(f'scraping URL {link}..')
            response.raise_for_status()
            ProxyScraper.process_response(response, link)
        except requests.RequestException:
            ProxyScraper.log('url [DOWN]')
            pass

    @staticmethod
    def process_response(response, url):
        soup = BeautifulSoup(response.text, 'html.parser')
        if "sslproxies" in url or "free-proxy-list" in url or "us-proxy" in url:
            table = soup.find('table', {'id': 'proxylisttable'}) or soup.find('table', {'class': 'table'})
            if table:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) > 1:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        if port.isdigit() and int(port) != 0:
                            ProxyScraper.add_proxy(f"{ip}:{port}", 'HTTP')
        elif "socks4" in url:
            for proxy in response.text.splitlines():
                parts = proxy.split(':')
                if len(parts) >= 2:
                    ip = parts[0].strip()
                    port = parts[1].strip()
                    if port.isdigit() and int(port) != 0:
                        ProxyScraper.add_proxy(f"{ip}:{port}", 'SOCKS4')
        elif "socks5" in url:
            for proxy in response.text.splitlines():
                parts = proxy.split(':')
                if len(parts) >= 2:
                    ip = parts[0].strip()
                    port = parts[1].strip()
                    if port.isdigit() and int(port) != 0:
                        ProxyScraper.add_proxy(f"{ip}:{port}", 'SOCKS5')
        elif "http" in url:
            for proxy in response.text.splitlines():
                parts = proxy.split(':')
                if len(parts) >= 2:
                    ip = parts[0].strip()
                    port = parts[1].strip()
                    if port.isdigit() and int(port) != 0:
                        ProxyScraper.add_proxy(f"{ip}:{port}", 'HTTP')

    @staticmethod
    def add_proxy(proxy, category):
        if proxy not in ProxyScraper.categories[category]:
            ProxyScraper.categories[category].append(proxy)
            ProxyScraper.total_proxies += 1


    @staticmethod
    def verify_proxy(proxy, category):

        try:
            response = requests.get(
                'https://www.google.com',
                proxies={category.lower(): f'{category.lower()}://{proxy}'},
                timeout=6
            )
            if response.status_code == 200:
                ProxyScraper.add_working_proxy(proxy, category)
                ProxyScraper.log(f"{colorama.Fore.GREEN}Proxy working: {proxy} ({category}){colorama.Fore.RESET}")
                return True
        except requests.RequestException:
            ProxyScraper.log(f"{colorama.Fore.RED}Proxy failed: {proxy} ({category}){colorama.Fore.RESET}")
        return False

    @staticmethod
    def remove_non_working_proxies():
        for category in ProxyScraper.categories:
            working_proxies = ProxyScraper.working_proxies[category]
            ProxyScraper.categories[category] = [
                proxy for proxy in ProxyScraper.categories[category]
                if proxy in working_proxies
            ]
            ProxyScraper.log(f"Removed non-working > {category} category.")


    @staticmethod
    def check_proxies():
        futures = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            for category, proxies in ProxyScraper.categories.items():
                for proxy in proxies:
                    futures.append(executor.submit(ProxyScraper.verify_proxy, proxy, category))

            for future in as_completed(futures):
                future.result()

    @staticmethod
    def add_working_proxy(proxy, category):
        if proxy not in ProxyScraper.working_proxies[category]:
            ProxyScraper.working_proxies[category].append(proxy)

    @staticmethod
    def save_proxies():
        for category, proxies in ProxyScraper.categories.items():
            if proxies:
                filename = f"{category.lower()}_proxies.txt"
                with open(filename, 'w') as f:
                    for proxy in proxies:
                        f.write(proxy + '\n')
                ProxyScraper.log(f"Saved {len(proxies)} {category} proxies to '{filename}'.")


if __name__ == "__main__":
    clear()
    colorama.init()
    ctypes.windll.kernel32.SetConsoleTitleW(' <<| Proxy Scraper BY >> [phantom-passwd] |>>')
    ProxyScraper.log("Starting proxy scraping...")
    ProxyScraper.scrape_proxies()
    ProxyScraper.save_proxies()
    ProxyScraper.clean_proxies()
    ProxyScraper.check_proxies()
    ProxyScraper.remove_non_working_proxies()
    ProxyScraper.log(f"Total proxies scraped: {ProxyScraper.total_proxies}")
