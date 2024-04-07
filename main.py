import requests
import smtplib

my_email = "zmssmzx@gmail.com"
password = "lyqi vxqn qfhq usty"
the_other_email = "xyz101abc321@yahoo.com"
email_juan = "juanfcr11@gmail.com"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "TDSJUCJ8MO3ZZDJK"
NEWS_API_KEY = "deba92ec9b0f410db3c47bbcbdbc5e10"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# NOW = str(dt.datetime.now())
# TODAY = NOW.split(" ")[0]

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price.
# Hint: You can perform list comprehensions on Python dictionaries.
# e.g. [new_value for (key, value) in dictionary.items()]
stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)

stock_response.raise_for_status()

stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
stock_data_yesterday = [key for (key, value) in stock_data.items()]

#  today = dt.date.today()
#  yesterday = str(today - dt.timedelta(days=1))
#  before_yesterday = str(today - dt.timedelta(days=2))
yesterday_data = stock_data_list[0]
yesterday_stock_close = float(yesterday_data["4. close"])

#TODO 2. - Get the day before yesterday's closing stock price
before_yesterday_data = stock_data_list[1]
before_yesterday_stock_close = float(before_yesterday_data["4. close"])

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp
stocks_difference = yesterday_stock_close - before_yesterday_stock_close
# abs_stocks_difference = abs(stocks_difference)
up_down = None
if stocks_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#TODO 4. - Work out the percentage difference in price
# between closing price yesterday and closing price the day before yesterday.

# x_percentage_difference = ((yesterday_stock_close * 100) / before_yesterday_stock_close) - 100
percentage_difference = round((stocks_difference / yesterday_stock_close) * 100)


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

# if percentage_difference > 5:
#     print("Get News")

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
news_data = []
if abs(percentage_difference) > 5:
    news_parameters = {
        "q": STOCK_NAME,
        "from": stock_data_yesterday,
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)

    news_response.raise_for_status()

    news_data = news_response.json()["articles"]

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles.
# Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
news_data_selection = news_data[:3]

# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
news_data_list = [(f"{STOCK_NAME}: {up_down}%\n"
                   f"Headline: {article['title']}.\n"
                   f"Brief: {article['description']}") for article in news_data_selection]

#TODO 9. - Send each article as a separate message via Twilio. 
for news in news_data_list:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email_juan,
            msg=f"Subject:{news[0]}\n\n{news[1]}"
        )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height 
of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height 
of the coronavirus market crash.
"""
