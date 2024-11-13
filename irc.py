from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import asyncio
import aiohttp
import itertools

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

target_url = ""
ip_list_urls = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
]

async def fetch_ip_addresses(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                text = await response.text()
                ip_addresses = text.splitlines()
                return ip_addresses
        except Exception as e:
            return []

async def get_all_ips():
    tasks = [fetch_ip_addresses(url) for url in ip_list_urls]
    ip_lists = await asyncio.gather(*tasks)
    all_ips = [ip for sublist in ip_lists for ip in sublist]
    return all_ips

async def send_request(ip_address):
    headers = {"X-Forwarded-For": ip_address}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, headers=headers) as response:
                result = f"Request sent to {target_url} from IP: {ip_address} - Status Code: {response.status}"
                socketio.emit('request_result', result)
    except Exception as e:
        error_result = f"Error sending request from IP: {ip_address} - {e}"
        socketio.emit('request_result', error_result)

async def main(num_requests):
    ip_list = await get_all_ips()
    ip_cycle = itertools.cycle(ip_list)
    tasks = [send_request(next(ip_cycle)) for _ in range(num_requests)]
    await asyncio.gather(*tasks)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
       
        print("POST request received")
        target_url = request.form.get("url")
        num_requests = int(request.form.get("num_requests"))
        asyncio.run(main(num_requests))
        return f"Requests sent to {target_url}"

    elif request.method == "GET":
        print("GET request received")
        return '''
            <form method="POST">
                <label for="url">Enter URL:</label>
                <input type="text" id="url" name="url" required>
                <br><br>
                <label for="num_requests">Enter number of requests:</label>
                <input type="number" id="num_requests" name="num_requests" required>
                <br><br>
                <button type="submit">Start Requests</button>
            </form>
        '''
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
