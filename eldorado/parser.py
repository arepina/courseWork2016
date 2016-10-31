import time
from bs4 import BeautifulSoup
import urllib.request

from db.DataBase_Eldorado import DataBase_Eldorado


def reviews(html, title_name):
    with urllib.request.urlopen(url_market + html) as url:
        review_html = url.read()
    soup = BeautifulSoup(review_html, "lxml")
    for review in soup.findAll("div", {"class": "middleBlockItem"}):  # get all categories from html file
        review_text = review.text
        review_text = review_text.replace("\n", " ")
        review_text = " ".join(review_text.split())
        print("\t\t" + review_text)
        dataBase.add_review(title_name, review_text)  # insert the review into data base


def sub_category(html, title_name):
    with urllib.request.urlopen(url_market + html) as url:
        sub_category_html = url.read()
    soup = BeautifulSoup(sub_category_html, "lxml")
    for review in soup.findAll("div", {"class": "reviews list"}):  # get all categories from html file
        review_link = review.find('a', href=True)['href']
        print("\t" + review_link)
        reviews(review_link, title_name)


def category(html):
    soup = BeautifulSoup(html, "lxml")
    for title in soup.findAll("div", {"class": "mainHitsItem catalogLvl2Item"}):  # get all categories from html file
        title_link = title.find('a', href=True)['href']
        title_name = title.find('a', href=True)['title']
        print(title_link + " " + title_name)
        sub_category(title_link, title_name)


dataBase = DataBase_Eldorado()
url_market = "http://www.eldorado.ru/"
start_url = "http://www.eldorado.ru/cat/2000/"  # the page we get categories from
with urllib.request.urlopen(start_url) as url:
    market_html = url.read()
category(market_html)
