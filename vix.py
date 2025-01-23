import json
import requests
import yfinance as yf
from datetime import datetime, timezone
from utils import delete_page, get_page_id, create_page

def get_vix(period = '30d'):
    vix = yf.Ticker("^VIX")
    data = vix.history(period = period).reset_index()
    close, date = (list(data["Close"]), list(data['Date'].apply(lambda x: x.astimezone(timezone.utc).isoformat())))
    return close, date

def create_data(closes, dates):
    all_data = []
    for close, date in zip(closes, dates):
        data = {
            "VIX": {"number": round(close, 4)},
            "Date": {"date": {"start": date}}
        }
        all_data.append(data)
    return all_data

def main():
    ids = get_page_id("vix")
    delete_page(ids, "vix")
    closes, dates = get_vix()
    all_data = create_data(closes, dates)
    create_page(all_data, "vix")

if __name__ == "__main__":
    main()