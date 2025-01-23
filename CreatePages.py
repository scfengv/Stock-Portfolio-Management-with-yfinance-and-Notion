import yfinance as yf
from utils import create_page, get_value

tickers = ["IGV", "IWM", "IYW"]
positions = [290, 40, 80]

def create_data():
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

def main():
    all_data = create_data()
    create_page(all_data, "portfolio")
    
if __name__ == "__main__":
    main()