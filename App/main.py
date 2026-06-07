import yfinance as yf

def run_backtest():
    cash = 10000
    shares = 0
    in_market = False
    buyhold_cash = 10000
    buyhold_shares = 0
    buyhold_bought = False
    history = []
    buyhold_history = []

    data = yf.download("TQQQ", start="2000-01-01")
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    data["SMA3"] = data["Close"].rolling(3).mean()
    data["SMA200"] = data["Close"].rolling(200).mean()
    data["Signal"] = ""
    data.loc[(data["SMA3"] < data["SMA200"]) & (data["SMA3"].shift(1) <= data["SMA200"].shift(1)), "Signal"] = "SELL"
    data.loc[(data["SMA3"] > data["SMA200"]) & (data["SMA3"].shift(1) >= data["SMA200"].shift(1)), "Signal"] = "BUY"
    print(data[data["Signal"] != ""])


    for date, row in data.iterrows():
        price = row["Close"]
        signal = str(row["Signal"])

        if buyhold_bought == False:
            buyhold_shares = buyhold_cash / price
            buyhold_bought = True
        
        buyhold_history.append(buyhold_shares * price)

        if signal == "SELL" and in_market == True:
            cash = shares * price
            shares = 0
            in_market = False
            print("Sold all shares")
        if signal == "BUY" and in_market == False:
            shares = cash / price
            cash = 0
            in_market = True
            print(f"Bought {shares} shares")
        
        if in_market == True:
            history.append(shares * price)
        if in_market == False:
            history.append(cash)


    if in_market == True:
        final_value = shares * price
    if in_market == False:
        final_value = cash
    buyhold_value = buyhold_shares * price
    dates = [str(d.date()) for d in data.index]
    return final_value, buyhold_value, history, buyhold_history, dates