import json
import requests
import yfinance as yf
from datetime import datetime, timezone

TOKEN = "TOKEN"
DBID = "ID"

headers = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages = None):
    url = f"https://api.notion.com/v1/databases/{DBID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json = payload, headers = headers)

    data = response.json()

    with open('db.json', 'w', encoding = 'utf8') as f:
       json.dump(data, f, ensure_ascii = False, indent = 4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DBID}/query"
        response = requests.post(url, json = payload, headers = headers)
        data = response.json()
        results.extend(data["results"])

    return results

def create_page(all_data: list):
    create_url = "https://api.notion.com/v1/pages"

    for data in all_data:
        payload = {"parent": {"database_id": DBID}, "properties": data}
        res = requests.post(create_url, headers = headers, json = payload)
        print(res.status_code)
    return res

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json = payload, headers = headers)
    return res

def get_value(tickers, positions):
    prices, values = [], []
    for ticker, position in zip(tickers, positions):
        stock = yf.Ticker(f"{ticker.upper()}")
        price = stock.info["previousClose"]
        value = position * price
        prices.append(price)
        values.append(value)
    return prices, values