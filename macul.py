import requests
import os
import re
import threading
import random
import argparse
import sys
import urllib.request
import logging
from time import time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Setup logging to a file for debugging
logging.basicConfig(filename='proxy_scraper.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Constants
output_file = 'proxy.txt'
proxy_urls = list(set([  # Removed duplicate URLs using a set
    'https://gist.github.com/DidanXx/54dd9d6ac7e5799312efac659aa8d91d#file-gistfile1-txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://gist.github.com/DidanXx/54dd9d6ac7e5799312efac659aa8d91d#file-gistfile1-txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/proxylist.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&prot'
    'https://api.proxyscrape.com/v2/?request=displayproxies',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://proxyspace.pro/http.txt',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'http://worm.rip/http.txt',
    'https://api.openproxylist.xyz/http.txt',
    'http://rootjazz.com/proxies/proxies.txt',
    'https://multiproxy.org/txt_all/proxy.txt',
    'https://proxy-spider.com/api/proxies.example.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
    'https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous',
    'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all',
    'https://api.proxyscrape.com/v2/?request=displayproxies',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
    'https://proxyspace.pro/http.txt',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'http://worm.rip/http.txt',
    'https://api.openproxylist.xyz/http.txt',
    'http://rootjazz.com/proxies/proxies.txt',
    'https://multiproxy.org/txt_all/proxy.txt',
    'https://proxy-spider.com/api/proxies.example.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
    'https://www.proxydocker.com/en/proxylist/download?email=noshare&country=all&city=all&port=all&type=all&anonymity=all&state=all&need=all',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/Firdoxx/proxy-list/main/https',
    'https://raw.githubusercontent.com/Firdoxx/proxy-list/main/http',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
    'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt',
    'https://raw.githubusercontent.com/casals-ar/proxy-list/main/http',
    'https://raw.githubusercontent.com/casals-ar/proxy-list/main/https',
    'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt',
    'https://raw.githubusercontent.com/Jakee8718/Free-Proxies/main/proxy/-http%20and%20https.txt',
    'https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/http.txt',
    'https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/https.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt',
    'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt',
    'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
    'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt',
    'https://github.com/hookzof/socks5_list/blob/master/proxy.txt',
    'https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies-http.txt',
    'https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies-https.txt',
    'https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies-socks4.txt',
    'https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies-socks5.txt',
    'https://github.com/jetkai/proxy-list/blob/main/online-proxies/txt/proxies.txt',
    'https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt',
    'https://checkerproxy.net/archive/2024-04-11',
    'https://checkerproxy.net/archive/2024-04-10',
    'https://checkerproxy.net/archive/2024-04-9',
    'https://checkerproxy.net/archive/2024-04-8',
    'https://checkerproxy.net/archive/2024-04-7',
    'https://checkerproxy.net/archive/2024-04-6',
    'https://checkerproxy.net/archive/2024-04-5',
    'https://checkerproxy.net/archive/2024-04-4',
    'https://checkerproxy.net/archive/2024-04-3',
    'https://checkerproxy.net/archive/2024-04-2',
    'https://checkerproxy.net/archive/2024-04-1',
    'https://checkerproxy.net/archive/2024-05-19',
    'https://checkerproxy.net/archive/2024-05-18',
    'https://checkerproxy.net/archive/2024-05-17',
    'https://checkerproxy.net/archive/2024-05-16',
    'https://checkerproxy.net/archive/2024-05-15',
    'https://checkerproxy.net/archive/2024-05-14',
    'https://checkerproxy.net/archive/2024-05-12',
    'https://checkerproxy.net/archive/2024-05-11',
    'https://checkerproxy.net/archive/2024-05-10',
    'https://checkerproxy.net/archive/2024-05-9',
    'https://checkerproxy.net/archive/2024-05-8',
    'https://checkerproxy.net/archive/2024-05-7',
    'https://checkerproxy.net/archive/2024-05-6',
    'https://checkerproxy.net/archive/2024-05-5',
    'https://checkerproxy.net/archive/2024-05-4',
    'https://checkerproxy.net/archive/2024-05-3',
    'https://checkerproxy.net/archive/2024-05-2',
    'https://checkerproxy.net/archive/2024-05-1',
    'https://checkerproxy.net/archive/2024-06-1',
    'https://checkerproxy.net/archive/2024-06-2',
    'https://checkerproxy.net/archive/2024-06-3',
    'https://checkerproxy.net/archive/2024-06-4',
    'https://checkerproxy.net/archive/2024-06-5',
    'https://checkerproxy.net/archive/2024-06-6',
    'https://checkerproxy.net/archive/2024-06-7',
    'https://checkerproxy.net/archive/2024-06-8',
    'https://checkerproxy.net/archive/2024-06-9',
    'https://checkerproxy.net/archive/2024-06-10',
    'https://checkerproxy.net/archive/2024-06-11',
    'https://checkerproxy.net/archive/2024-06-12',
    'https://checkerproxy.net/archive/2024-06-13',
    'https://checkerproxy.net/archive/2024-06-14',
    'https://checkerproxy.net/archive/2024-06-15',
    'https://checkerproxy.net/archive/2024-06-16',
    'https://checkerproxy.net/archive/2024-06-17',
    'https://checkerproxy.net/archive/2024-06-18',
    'https://checkerproxy.net/archive/2024-06-19',
    'https://checkerproxy.net/archive/2024-06-20',
    'https://checkerproxy.net/archive/2024-07-1',
    'https://checkerproxy.net/archive/2024-07-2',
    'https://checkerproxy.net/archive/2024-07-3',
    'https://checkerproxy.net/archive/2024-07-4',
    'https://checkerproxy.net/archive/2024-07-5',
    'https://checkerproxy.net/archive/2024-07-6',
    'https://checkerproxy.net/archive/2024-07-7',
    'https://checkerproxy.net/archive/2024-07-8',
    'https://checkerproxy.net/archive/2024-07-9',
    'https://checkerproxy.net/archive/2024-07-10',
    'https://checkerproxy.net/archive/2024-07-11',
    'https://checkerproxy.net/archive/2024-07-12',
    'https://checkerproxy.net/archive/2024-07-13',
    'https://checkerproxy.net/archive/2024-07-14',
    'https://checkerproxy.net/archive/2024-07-15',
    'https://checkerproxy.net/archive/2024-07-16',
    'https://checkerproxy.net/archive/2024-07-17',
    'https://checkerproxy.net/archive/2024-07-17',
]))

# Clear console
os.system('cls' if os.name == 'nt' else 'clear')

# Remove existing output file if present
if os.path.isfile(output_file):
    os.remove(output_file)
    print(f"{Fore.RED}'proxy.txt' telah dihapus.{Fore.RESET}")

print(f"{Fore.YELLOW}Otw Download\n")

def download_and_save_proxies(url, output_file):
    """Download proxies from the given URL and save to output file."""
    try:
        session = requests.Session()
        retry = requests.adapters.Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(url)
        if response.status_code == 200:
            with open(output_file, 'a') as file:
                file.write(response.text)
            print(f"{Fore.GREEN}Collect {Fore.WHITE}{url} {Fore.GREEN}")
            logging.info(f"Successfully downloaded proxies from {url}")
        else:
            print(f"{Fore.RED}Gagal {url}{Fore.RESET}")
            logging.error(f"Failed to download {url} with status code: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}Gagal {url}{Fore.RESET}")
        logging.error(f"Exception occurred while downloading {url}: {e}")

# Clear the output file
open(output_file, 'w').close()

class Proxy:
    def __init__(self, method, proxy):
        if method.lower() not in ["http", "https"]:
            raise NotImplementedError("Only HTTP and HTTPS are supported")
        self.method = method.lower()
        self.proxy = proxy

    def is_valid(self):
        return re.match(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?$", self.proxy)

    def check(self, site, timeout, user_agent):
        """Check if the proxy is valid by sending a request through it."""
        url = self.method + "://" + self.proxy
        proxy_support = urllib.request.ProxyHandler({self.method: url})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(self.method + "://" + site)
        req.add_header("User-Agent", user_agent)
        try:
            start_time = time()
            urllib.request.urlopen(req, timeout=timeout)
            end_time = time()
            time_taken = end_time - start_time
            return True, time_taken, None
        except Exception as e:
            return False, 0, e

    def __str__(self):
        return self.proxy

def verbose_print(verbose, message):
    """Prints a message if verbose mode is enabled."""
    if verbose:
        print(message)

def check_proxies(file, timeout, method, site, verbose, random_user_agent):
    """Check the proxies from the file and filter out valid ones."""
    proxies = []
    valid_proxies = []
    
    # Load proxies from file
    with open(file, "r") as f:
        for line in f:
            proxies.append(Proxy(method, line.strip()))
    
    print(f"{Fore.GREEN}Checking {Fore.YELLOW}{len(proxies)} {Fore.GREEN}Proxy")
    proxies = list(filter(lambda x: x.is_valid(), proxies))  # Filter only valid proxies
    
    user_agent = random.choice(user_agents)  # Random user agent selection

    def check_proxy(proxy, user_agent):
        """Check a single proxy and append if valid."""
        if random_user_agent:
            user_agent = random.choice(user_agents)
        valid, time_taken, error = proxy.check(site, timeout, user_agent)
        if valid:
            valid_proxies.append(proxy)
            message = f"{proxy} is valid, took {time_taken:.2f} seconds"
        else:
            message = f"{proxy} is invalid: {repr(error)}"
        verbose_print(verbose, message)

    # Use ThreadPoolExecutor to manage threads efficiently
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda proxy: check_proxy(proxy, user_agent), proxies)

    # Save valid proxies back to the file
    with open(file, "w") as f:
        for proxy in valid_proxies:
            f.write(str(proxy) + "\n")
    
    print(f"{Fore.GREEN}Found {Fore.YELLOW}{len(valid_proxies)} {Fore.GREEN}valid proxies")
    logging.info(f"Found {len(valid_proxies)} valid proxies")

# Download proxies from all URLs
for url in proxy_urls:
    download_and_save_proxies(url, output_file)

# Count the number of proxies downloaded
with open(output_file, 'r') as ceki:
    total_proxies = sum(1 for line in ceki)
    
print(f"\n{Fore.WHITE}( {Fore.YELLOW}{total_proxies} {Fore.WHITE}) {Fore.GREEN}Proxy Sudah Di Unduh, Mau Check? {Fore.WHITE}({Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}N{Fore.WHITE}): ", end="")
choice = input().strip().lower()

if choice == 'y':
    # User agent list
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    ]

    # Argument parser for command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timeout", type=int, default=20, help="Dismiss the proxy after -t seconds")
    parser.add_argument("-p", "--proxy", default="http", help="Check HTTPS or HTTP proxies")
    parser.add_argument("-s", "--site", default="https://google.com/", help="Check with specific website like google.com")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("-r", "--random_agent", action="store_true", help="Use a random user agent per proxy")
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check proxies
    check_proxies(file=output_file, timeout=args.timeout, method=args.proxy, site=args.site, verbose=args.verbose, random_user_agent=args.random_agent)
else:
    print(f"{Fore.YELLOW}fiftyseven x chocho 4 ever.\n")
