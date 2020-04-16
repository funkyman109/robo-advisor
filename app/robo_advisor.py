#base taken from prof rossetti https://www.youtube.com/watch?v=UXAVOP1oCog
import csv
import json
import os
import pandas as pd
import re
import sys
import datetime

from dotenv import load_dotenv
import requests

load_dotenv()

def to_usd(price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${price:,.2f}" #> $12,000.71

def get_response(symbol, api_key):
    """
    will pull stock information from api based on ticker symbol
    """
    pull = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}")
    return pull

def parsed_answer(response):
    """
    will format requested data in a json loaded format
    """
    output= response.text
    parsed_response = json.loads(output)
    return parsed_response

def write_csv(csv_file_path, csv_headers):
   """
   writes currently existing json data into a csv file to be used later
   """
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for date in dates:
            daily_prices= tsd[date]
            writer.writerow({
                "timestamp": date,
                "open": daily_prices['1. open'],
                "high": daily_prices['2. high'],
                "low": daily_prices['3. low'],
                "close": daily_prices['4. close'],
                "volume": daily_prices['5. volume'],
            })

#info inputs


if __name__ == "__main__":

    Daytime = datetime.datetime.now()

    api_key = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

    #taken from https://stackoverflow.com/questions/8761778/limiting-python-input-strings-to-certain-characters-and-lengths
    symbol = input("Please enter the ticker of your stock of choice: ")
    if not re.match("^[a-z]*$", symbol):
        print("Error! Only letters a-z allowed!")
        sys.exit()
    elif len(symbol) > 5:
        print("Error! Only 5 characters allowed!")
        sys.exit()

    response = get_response(symbol, api_key)
    parsed_response = parsed_answer(response)
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    tsd = parsed_response['Time Series (Daily)']
    dates = list(tsd.keys())
    latest_date = dates[0]
    latest_close = to_usd(float(tsd[latest_date]['4. close']))

    high_prices = []
    for date in dates:
        high_price = float(tsd[date]['2. high'])
        high_prices.append(high_price)
    recent_high = to_usd(max(high_prices))

    low_prices = []
    for date in dates:
        low_price = float(tsd[date]['3. low'])
        low_prices.append(low_price)
    recent_low = to_usd(min(low_prices))

    #info outputs

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    csv_headers = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

    write_csv(csv_file_path,csv_headers)


    #making recommendation
    #pandas indformation taken from https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/pandas.md
    stock_info = pd.read_csv(csv_file_path)
   

    # retrieving variables from csv
    close = stock_info["close"][0]
    ll = stock_info["low"].min()
    hh = stock_info["high"].max()
    

    #creating a lower boundary in order to analyze volatility
    #idea taken from summer internship 

    lower_boundary = close * 0.75
    upper_boundary = close * 1.64

    if ll < lower_boundary or hh > upper_boundary:
        rec = "Don't Buy."
        reason = "Stock appears to be very volatile. Thus, it is a risk to your portfolio."
    else:
        rec = "Buy it Baby."
        reason = "Stock is not volatile and likely to continue on its current trend."


  #printing out advice for the app user

    print("-------------------------")
    print("SELECTED SYMBOL:", symbol)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT:", Daytime)
    print("-------------------------")
    print("LATEST DAY:", last_refreshed)
    print("LATEST CLOSE:", latest_close)
    print("RECENT HIGH:", recent_high)
    print("RECENT LOW:", recent_low)
    print("-------------------------")
    print("RECOMMENDATION:", rec)
    print("RECOMMENDATION REASON:", reason)
    print("-------------------------")
    print("writing data to csv file:", csv_file_path)
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

