import pandas as pd
import yfinance as yf
import requests
import time
import random
from sentiment_analysis import analyze_sentiment


# Get Information from excel


path_cash_pos = "data\client-data\Swiss AI - UBS Challenge 3 - Cash Positions.xlsx"
path_portfolio_pos = "data\client-data\Swiss AI - UBS Challenge 3 - Portfolio Positions.xlsx"
cash_pos_df = pd.read_excel(path_cash_pos)
portfolio_pos_df = pd.read_excel(path_portfolio_pos)

partner_id = "OEM4B4lTFX"
account_number_unique_list = portfolio_pos_df[portfolio_pos_df["Partner ID Fake"] == partner_id]["Account ID Fake"].unique()

ticker_list_unique = []

for acnt_nr in account_number_unique_list:
    ISIN_list = portfolio_pos_df[portfolio_pos_df["Account ID Fake"] == acnt_nr]["ISIN"]
    for ISIN in ISIN_list.unique():
        try:
            data = yf.Ticker(str(ISIN))
            ticker = data.ticker
            ticker_list_unique.append(ticker)


            #news = data.news
            #current_news = news[news[{}]]
            '''
            for article in news:
                url = article["content"]["canonicalUrl"]["url"]
                if not url == "":
                    response = requests.get(url)
                    retry_count = 1
                    while response.status_code == 429 and retry_count <= 10:
                        try:
                            retry_after = int(response.headers.get("Retry-After"))  # default 60 sec
                            print(f"Too many requests. Retrying in {retry_after} seconds...")
                            time.sleep(retry_after)
                            response = requests.get(url)
                        except:
                            retry_after = random.uniform(1, 5)
                            print(f"Too many requests. Retrying in {retry_after} seconds...")
                            time.sleep(retry_after)
                            response = requests.get(url)
                        retry_count += retry_count
                    article_content = response.text

                    print(article_content)
                    '''
        except ValueError:
            news = "This ISIN is not real."


    sentiment_result = analyze_sentiment(ticker_list_unique,"I'm a conservative investor with aiming for long-term investment horizon")





