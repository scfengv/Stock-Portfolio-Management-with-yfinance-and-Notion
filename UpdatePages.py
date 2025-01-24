import json
import yfinance as yf
from utils import update_page, get_value, get_pages, create_page, delete_page

with open("StockPort.json", "r") as file:
    current_data = json.load(file)
    
tickers = list(current_data.keys())
positions = list(current_data.values())

def create_data(tickers, positions):
    all_data = []
    prices, values = get_value(tickers, positions)
    for ticker, position, value, price in zip(tickers, positions, values, prices):
        data = {
            "Ticker": {"title": [{"text": {"content": ticker}}]},
            "Market Value": {"number": round(value, 0)},
            "Position": {"number": position},
            "Price": {"number": price}
        }
        all_data.append(data)
    return all_data


def main(tickers):
    """
    1. Get stock information & ids in Notion
    2. Buy new stock
        If stock info (O) but id (X):
            Create new pages
    3. Position Change
        If stock info (O) & id (O):
            Update pages
    4. Sell stock
        If stock info (X) but id (O):
            Delete pages
    """
    results = get_pages("portfolio", None)
    notion_data = {
        result["properties"]["Ticker"]["title"][0]["text"]["content"]: result["id"]
        for result in results
    }
    notion_tickers = set(notion_data.keys())
    current_tickers = set(tickers)
    
    # Buy new stocks (in current list but not in Notion)
    new_stocks = current_tickers - notion_tickers
    if new_stocks:
        positions = [current_data[new] for new in new_stocks]
        new_data = create_data(new_stocks, positions)
        create_page(new_data, "portfolio")
    
    # Position Change (existing stocks)
    same_stocks = current_tickers & notion_tickers
    if same_stocks:
        positions = [current_data[same] for same in same_stocks]
        ids = list(notion_data.values())
        new_data = create_data(same_stocks, positions)
        update_page(ids, new_data, "portfolio")
    
    # Sell stocks (in Notion but not in current list)
    sell_stocks = notion_tickers - current_tickers
    if sell_stocks:
        ids = [notion_data[sell] for sell in sell_stocks]
        delete_page(ids, "portfolio")

if __name__ == "__main__":
    main(tickers)