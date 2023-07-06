import asyncio
import requests_async as requests
from flask import Flask, request

app = Flask(__name__)


async def send_request(url):
    response = await requests.get(url, verify=False)
    print(response.status_code)


@app.route("/webhook-test", methods=["POST"])
def webhook():
    print("Webhook received")
    data = request.get_json()
    urls = [
        "https://www.google.com",
        "https://www.facebook.com",
        "https://www.youtube.com",
    ]

    async def main():
        tasks = [send_request(url) for url in urls]
        await asyncio.gather(*tasks)
        
    asyncio.run(main())
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)