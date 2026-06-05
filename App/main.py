import yfinance as yf

data = yf.download("SPY", start="2020-01-01")
print(data)
