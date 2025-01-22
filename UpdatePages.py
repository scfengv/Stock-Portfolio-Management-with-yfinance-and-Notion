import yfinance as yf
from utils import update_page, get_value, get_pages

tickers = ["IGV", "IWM", "IYW"]
positions = [290, 40, 80]

def get_page_id():
    ids = []
    results = get_pages()
    for ticker in tickers:
        for result in results:
            if result["properties"]["Ticker"]["title"][0]["text"]["content"] == ticker:
                ids.append(result["id"])
    return ids

def main():
    ids = get_page_id()
    prices, values = get_value(tickers, positions)
# if __name__ == "__main__":