import requests
from twilio.rest import Client

"""Use the name of the stock and name of the company, for example: IBM"""
STOCK_NAME = "IBM"
COMPANY_NAME = "IBM Inc"

"""get the stock prices from www.alphavantage.co by putting api key in MY_API"""
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
MY_API = ""

"""put the news api key in NEWS_API to get news from newsapi.org"""
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = ""

"""use your own twilio sid and auth token to send the stock news as a text message"""
TWILIO_SID = ""
TWILIO_AUTH = ""
par = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": MY_API,
}

"""get the latest closing price of a particular stock"""
res = requests.get(STOCK_ENDPOINT, params=par)
res.raise_for_status()
stock = res.json()["Time Series (Daily)"]
price_list = [value for (key, value) in stock.items()]
last_data = price_list[0]
last_closing_price = price_list["4. close"]


"""getting the day before yesterday's closing price"""
second_last_data = price_list[1]
second_closing_price = price_list ["4. close"]

"""Compare the two prices and find the difference of two prices"""
price_contrast = float(last_closing_price) - float(second_closing_price)
emoji = None
if price_contrast > 0:
    emoji = "UP⬆️"
else:
    emoji = "DOWN⬇️"
percentage_of_contrast = round((price_contrast / float(last_closing_price)) * 100)

"""if the percentage of price difference is more than 3 percent, search for relevant news using News api"""
if abs(percentage_of_contrast) > 3:
    param_newsapi = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
    }
    res_news = requests.get(NEWS_ENDPOINT, params=param_newsapi)
    all_articles = res_news.json()["articles"]
    """get the first two articles related to the news of the stock"""
    first_two_news = all_articles[:2]
    """format the two articles for the message, which will be received by the user"""
    article_message = [f"{STOCK_NAME} is {emoji} by {percentage_of_contrast} % ,NEWS: {article['title']}. \nDescription:{article['description']}" for article in first_two_news]

    """put your Twilio virtual number in 'from' number, and put the user/customer number in 'to' number"""
    user = Client(TWILIO_SID, TWILIO_AUTH)
    for article in article_message:
        message = user.messages.create(
            body=article,
            from="",
            to="",
        )


