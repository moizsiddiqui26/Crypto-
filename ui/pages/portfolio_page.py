def calculate_metrics(row):
    symbol = row["Crypto"]
    invested = row["Amount Invested"]
    # 1. Convert input date to a standard string format 'YYYY-MM-DD'
    buy_date_str = str(row["Date"]) 
    
    try:
        hist_df = df.copy()
        # 2. Ensure the historical DF dates are also in 'YYYY-MM-DD' string format
        hist_df['Date'] = pd.to_datetime(hist_df['Date']).dt.strftime('%Y-%m-%d')
        
        # 3. Filter using string comparison
        match = hist_df[(hist_df['Crypto'] == symbol) & (hist_df['Date'] == buy_date_str)]
        
        if not match.empty:
            buy_price = float(match.iloc[0]['Close'])
        else:
            # If date is not found in history, use the oldest available price for that coin
            coin_history = hist_df[hist_df['Crypto'] == symbol]
            buy_price = float(coin_history.iloc[0]['Close']) if not coin_history.empty else live_prices.get(symbol, 0)
    except Exception as e:
        buy_price = live_prices.get(symbol, 0)

    # 4. Get Current Price from live state
    current_price = live_prices.get(symbol, buy_price)
    
    # 5. Performance Logic
    tokens = invested / buy_price if buy_price > 0 else 0
    current_value = tokens * current_price
    profit = current_value - invested
    pct_change = (profit / invested * 100) if invested > 0 else 0
    
    return pd.Series([buy_price, current_price, profit, pct_change])
