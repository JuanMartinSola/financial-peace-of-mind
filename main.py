import pandas as pd
import yfinance as yf
import requests
import time
import random
from sentiment_analysis import analyze_sentiment
from news_scrapper import news_scrapper
from datetime import datetime, timedelta
import scrapy
from scrapy.crawler import CrawlerProcess
from auxfunctions import get_urls


# Get Information from excel


path_cash_pos = "data\client-data\Swiss AI - UBS Challenge 3 - Cash Positions.xlsx"
path_portfolio_pos = "data\client-data\Swiss AI - UBS Challenge 3 - Portfolio Positions.xlsx"
cash_pos_df = pd.read_excel(path_cash_pos)
portfolio_pos_df = pd.read_excel(path_portfolio_pos)

class DynamicSpider(scrapy.Spider):
    name = "dynamic_spider"

    def __init__(self, urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls

    def parse(self, response):
        # Save each page HTML to a file
        filename = response.url.strip("/").split("/")[-1] or "index"
        filename = f"{filename}.html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"Saved {filename}")

# -----------------------------
# Main function to start the crawler
# -----------------------------
def main():
    partner_id = "OEM4B4lTFX"
    account_number_unique_list = portfolio_pos_df[portfolio_pos_df["Partner ID Fake"] == partner_id][
        "Account ID Fake"].unique()

    ticker_list_unique = []

    # Calculate the beginning of yesterday
    today = datetime.utcnow().date()  # today's date in UTC
    beginning_of_yesterday = datetime.combine(today - timedelta(days=1), datetime.min.time())

    for acnt_nr in account_number_unique_list:
        ISIN_list = portfolio_pos_df[portfolio_pos_df["Account ID Fake"] == acnt_nr]["ISIN"]
        for ISIN in ISIN_list.unique():
            try:
                data = yf.Ticker(str(ISIN))
                ticker = data.ticker
                ticker_list_unique.append(ticker)

                news = data.news

                # Parse strings and filter
                current_news = [
                    article for article in news
                    if
                    datetime.strptime(article["content"]['displayTime'], "%Y-%m-%dT%H:%M:%SZ") >= beginning_of_yesterday
                ]

                urls = get_urls(current_news)


                for article in current_news:
                    url = article["content"]["canonicalUrl"]["url"]
                    if not url == "":
                        response = requests.get(url)
                        retry_count = 1
                        if response.status_code == 429:
                            while response.status_code == 429 and retry_count <= 10:
                                try:
                                    retry_after = int(response.headers.get("Retry-After"))  # default 60 sec
                                    print(f"Too many requests. Retrying in {retry_after} seconds...")
                                    time.sleep(retry_after)
                                    response = requests.get(url)
                                    if response.status_code == 429:
                                        break
                                except:
                                    retry_after = random.uniform(1, 5)
                                    print(f"Too many requests. Retrying in {retry_after} seconds...")
                                    time.sleep(retry_after)
                                    response = requests.get(url)
                                    if response.status_code == 429:
                                        break
                                retry_count += retry_count
                        article_content = response.text

                        print(article_content)
            except ValueError:
                news = "This ISIN is not real."



    # Scrapy settings
    settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 10,
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_DELAY": 1,
        "RETRY_HTTP_CODES": [429, 500, 502, 503, 504],
        "RETRY_TIMES": 5,
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
        },
        # Uncomment and configure proxies if needed
        # "ROTATING_PROXY_LIST": [
        #     "http://user:pass@proxy1:8000",
        #     "http://user:pass@proxy2:8000",
        # ],
        # "DOWNLOADER_MIDDLEWARES.update": {
        #     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        #     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        # },
    }

    # Start crawler
    '''
    process = CrawlerProcess(settings)
    process.crawl(DynamicSpider, urls=urls)
    process.start()
    '''


    #sentiment_result = analyze_sentiment(ticker_list_unique,"I'm a conservative investor with aiming for long-term investment horizon")
    #query = "OR".join(ticker_list_unique)
    #scrapper_result = news_scrapper(query)

if __name__ == "__main__":
    main()
