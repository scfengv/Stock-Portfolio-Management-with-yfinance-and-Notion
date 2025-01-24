import json
import requests
import yfinance as yf
from datetime import datetime, timezone

portfolio_token = "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"
portfolio_id = "183e24f6f1458059ac3bd172b76bd120"

vix_token = "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"
vix_id = "183e24f6f14580709b3ef829f315397f"

portfolio_headers = {
    "Authorization": "Bearer " + portfolio_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

vix_headers = {
    "Authorization": "Bearer " + vix_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def select_task(task):
    if task == "portfolio":
        (id, token, headers) = (portfolio_id, portfolio_token, portfolio_headers)
    elif task == "vix":
        (id, token, headers) = (vix_id, vix_token, vix_headers)
    else:
        raise Exception("Invalid task")
    return (id, token, headers)
        
def get_pages(task, num_pages = None):
    id, token, headers = select_task(task)
    url = f"https://api.notion.com/v1/databases/{id}/query"
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    payload = {"page_size": page_size}
    response = requests.post(url, json = payload, headers = headers)

    data = response.json()
    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{id}/query"
        response = requests.post(url, json = payload, headers = headers)
        data = response.json()
        results.extend(data["results"])
    return results

def create_page(all_data: list, task):
    create_url = "https://api.notion.com/v1/pages"
    id, token, headers = select_task(task)
    for data in all_data:
        payload = {"parent": {"database_id": id}, "properties": data}
        response = requests.post(create_url, json = payload, headers = headers)
        print(response.status_code)
    return response

def update_page(page_ids: list, all_data: list, task):
    id, token, headers = select_task(task)
    for page_id, data in zip(page_ids, all_data):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"properties": data}
        response = requests.patch(url, json = payload, headers = headers)
        print(response.status_code)
    return response

def delete_page(page_ids: list, task):
    id, token, headers = select_task(task)
    for page_id in page_ids:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"archived": True}
        response = requests.patch(url, json = payload, headers = headers)
        print(response.status_code)
    return response

def get_page_id(task):
    ids = []
    results = get_pages(task = task, num_pages = None)
    for result in results:
        ids.append(result["id"])
    return ids

def get_value(tickers, positions):
    prices, values = [], []
    for ticker, position in zip(tickers, positions):
        rate = 1
        stock = yf.Ticker(f"{ticker.upper()}")
        price = stock.info["previousClose"]
        if stock.info["currency"] != "USD":
            rate = get_currency_rate(base_currency = stock.info["currency"])
        value = position * price * rate
        prices.append(price)
        values.append(value)
    return prices, values

def get_currency_rate(base_currency, target_currency = "USD"):
    key = "e341459d838343f783ffa249"
    try:
        url = f"https://v6.exchangerate-api.com/v6/{key}/latest/{base_currency}"
        
        response = requests.get(url)
        data = response.json()
        
        if data["result"] == "success":
            rate = data["conversion_rates"][target_currency]
            return rate
        else:
            print("Error fetching exchange rate")
            return None
    
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return None