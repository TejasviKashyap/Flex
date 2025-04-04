import streamlit as st
from langchain_core.tools import tool
from typing import List

@tool(return_direct=True)
def get_stock_data(stocks: List[str], period: str) -> dict:
    """
    Fetches comprehensive stock data for given symbols and returns it as a List of dictionaries.
    """
    import yfinance as yf
    
    stock_symbol = []
    for s in stocks:
        res = yf.Search(s, max_results=1).quotes
        sym = None
        if isinstance(res, list) and len(res) == 1:
            stock_symbol.append(res[0]['symbol'])
    
    if period not in ['1d', '5d', '1mo']:
        period = "5d"

    stocks = yf.Tickers(" ".join(stock_symbol))
    st_info = {}
    for s in stocks.tickers:
        info = stocks.tickers[s].info
        history = stocks.tickers[s].history(period=period).to_dict()
        combined_data = {
            "info": info,
            "history": history
        }
        st_info[s] = combined_data
    return st_info



@tool(return_direct=True)
def lookup_forex_rates(src: str, dest: str) -> str:
    """
    Get the forex rate for a given source and destination currency.
    """
    import requests
    
    api_url = "https://www.alphavantage.co/query"
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": src,
        "to_currency": dest,
        "apikey": "CB49E2GZ2D3YZ7DT"  # This is a placeholder, should be replaced with a proper API key
    }

    response = requests.get(api_url, params=params, timeout=30)
    data = response.json()

    if "Realtime Currency Exchange Rate" in data:
        rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        return f"1 {src} is worth {rate} {dest}."
    else:
        return "Currency conversion rate not found."