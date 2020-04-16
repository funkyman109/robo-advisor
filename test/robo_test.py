import csv
import json
import os
import pandas as pd
import re
import sys
import datetime

from dotenv import load_dotenv
import requests

from app.robo_advisor import to_usd, get_response, parsed_answer, write_csv

def test_to_usd():
    result = to_usd(3.47)
    assert result == f"${3.47:,.2f}"

def test_getresponse():
    symbol = "AAPL"
    api_key = str(os.environ.get("ALPHAVANTAGE_API_KEY"))
    #pull1 = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=" + apikey)

    answer = get_response(symbol, api_key)

    parsed_answer = json.loads(answer.text)
    result = list(parsed_answer)

    assert result == ['Meta Data', 'Time Series (Daily)']

def test_parsedanswer():
    symbol = "AAPL"
    api_key = str(os.environ.get("ALPHAVANTAGE_API_KEY"))
    pull1 = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}")

    #answer = get_response(symbol, api_key)

    parsed = parsed_answer(pull1)
    result = list(parsed)

    assert result == ['Meta Data', 'Time Series (Daily)']

#taken from https://www.guru99.com/python-check-if-file-exists.html
def test_csv_writer():
    symbol = "AAPL"
    api_key = str(os.environ.get("ALPHAVANTAGE_API_KEY"))
    response = get_response(symbol, api_key)
    parsed_response = parsed_answer(response)
    tsd = parsed_response['Time Series (Daily)']
    dates = list(tsd.keys())
    latest_date = dates[0]
    latest_close = to_usd(float(tsd[latest_date]['4. close']))
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    csv_headers = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    write_csv(csv_file_path,csv_headers)
    assert str(os.path.exists(csv_file_path)) == True