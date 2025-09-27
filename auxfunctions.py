import requests
import time
import random


def get_urls(news):
    url_list = []
    for article in news:
        url = article["content"]["canonicalUrl"]["url"]
        if not url == "":
            url_list.append(url)
    return url_list
