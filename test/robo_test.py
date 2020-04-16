import csv
import json
import os
import pandas as pd
import re
import sys
import datetime

from dotenv import load_dotenv
import requests

from app.robo_advisor import to_usd, get_response, parsed_answer

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