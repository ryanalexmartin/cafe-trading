# We want to backtest and trade TSLA stock data.
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from fugle_marketdata import RestClient
from fugle_marketdata import WebSocketClient, RestClient
from datetime import datetime, timedelta
import pandas as pd

fugle_api_key = "YOUR_FUGLE_API_KEY"  # Replace with your Fugle API key

class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

def get_historical_data(symbol, lookback_days=30):

    # Date range must be less than one year.
    if lookback_days > 365:
        raise ValueError("Lookback period must be less than or equal to 365 days.")

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_days)
    
    # Initialize client
    client = RestClient(api_key=fugle_api_key)
    stock = client.stock  # Stock REST API client
    
    # Get historical candles
    response = stock.historical.candles(**{"symbol": symbol,
                                           "from": start_date.strftime('%Y-%m-%d'),
                                           "to": end_date.strftime('%Y-%m-%d'),
                                           "fields": "open,high,low,close,volume"})
    print(response)

    # Convert to pandas DataFrame
    df = pd.DataFrame(response['data'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)  # Sort by date ascending

    # Rename columns to match backtesting library
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)
    
    return df


bt = Backtest(get_historical_data('2330', 364), 
              SmaCross,
              cash=10000, 
              commission=.002,
              exclusive_orders=True)

output = bt.run()
bt.plot()