import requests
import pandas as pd
import time

# Example: Alpha Vantage API Key and URL
API_KEY = '7268H1Y3MI0OMWLP'
symbol = 'TSLA'
api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'

def fetch_stock_data():
    response = requests.get(api_url)
    data = response.json()
    time_series = data['Time Series (1min)']
    
    # Convert to DataFrame for Pandas processing
    df = pd.DataFrame.from_dict(time_series, orient='index', dtype=float)
    df.index = pd.to_datetime(df.index)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    return df

# Fetch and display data
df = fetch_stock_data()
print(df.head())

def process_data(df):
    # Calculate Moving Averages for trends
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_30'] = df['Close'].rolling(window=30).mean()
    
    return df

processed_data = process_data(df)
print(processed_data.tail())

def update_data(df):
    while True:
        new_data = fetch_stock_data()
        df = pd.concat([df, new_data]).drop_duplicates()
        
        # Re-process the data after each update
        df = process_data(df)
        
        time.sleep(60)  # Fetch new data every minute

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)
])

@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Fetch new data and process it
    df = fetch_stock_data()
    df = process_data(df)
    
    # Create the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Stock Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_10'], mode='lines', name='SMA 10'))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_30'], mode='lines', name='SMA 30'))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

import ctypes

# Load the C++ shared library
cpp_lib = ctypes.CDLL('./moving_average.so')

# Example of calling C++ moving average function from Python
data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
window = 3

# Convert Python list to C array and call the C++ function
result = cpp_lib.moving_average(ctypes.c_double * len(data), ctypes.c_int(window))
