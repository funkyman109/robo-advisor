# robo-advisor

This application is designed to help you pick stocks that will make you a millionaire. Our predictions are based off of volatility

## setup instructions
first dowload our repo and navigate there using your command line.

```sh
cd ~/Desktop/robo-advisor
```

create a virtual environment with the packages and modules you will need to run our app

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

after creating this environment, go ahead and install all the packages found in our "requirements.txt" file

```sh
pip install -r requirements.txt
```

## running the app

at this point you should be able to run our application without any hiccups. We recommend that you research the ticker of your desired stock before commencing

```sh
python app/robo_advisor.py
```

when prompted for the stock symbol (ticker) please enter the 1-5 letter symbol in all lower-case letters.

You should now have your answer and additional data on the recent activity of your selected stock has been stored in a csv file names "prices.csv.

Have a good day and we hope you found us helpful.