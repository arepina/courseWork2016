import time
from bs4 import BeautifulSoup
import urllib.request

from db.DataBase_Ulmart import DataBase_Ulmart


def category(start_url):
    with urllib.request.urlopen(start_url) as url:
        market_html = url.read()
    soup = BeautifulSoup(market_html, "lxml")
    for title in soup.findAll("div", {"class": "b-product__art"}):  # get all products
        article = title.find('span').text
        print(article)
        completed = False
        while not completed:
            try:
                product(article)
                completed = True
            except:
                print("error, try again")


def product(article):
    reviews_num = dataBase.reviews_num(article)
    if reviews_num != None:
        reviews_num = reviews_num[0]
    else:
        reviews_num = 0
    new_url = "https://www.ulmart.ru/goods/" + article + "/reviews"
    with urllib.request.urlopen(new_url) as url:
        market_html = url.read()
    soup = BeautifulSoup(market_html, "lxml")
    reviews = soup.findAll("ul", {"class": "b-list b-list_theme_normal b-list_title-left b-list_review"})
    if reviews_num == len(reviews):
        return
    reviews = reviews[reviews_num:]
    for review in reviews:  # get all reviews from concrete product
        adv = 'Null'
        dis = 'Null'
        com = 'Null'
        for review_part in review.findAll("li", {"class": "b-list__item"}):  # get all categories from html file
            name = review_part.find('span').text
            if name == "Достоинства":
                adv = review_part.find('div').text
            elif name == "Недостатки":
                dis = review_part.find('div').text
            elif name == "Общие впечатления":
                com = review_part.find('div').text
        dataBase.add_review(article, adv, dis, com)


dataBase = DataBase_Ulmart()
url_market = "https://www.ulmart.ru/"
start_url = "https://www.ulmart.ru/catalogAdditional/brand_computers?sort=5&viewType=1&destination=&extended=&filters=&numericFilters=&brands=&jdSuppliers=&warranties=&bargainTypes=&priceColors=&receiptTime=&minWarranty=&maxWarranty=&shops=&labels=&available=&reserved=&suborder=&availableCounts=&superPrice=&showCrossboardGoods=&showUlmartGoods=&specOffers=&minPrice=&maxPrice=&query=&pageNum="  # the page we get categories from
nums = [x for x in range(1, 6)]
for num in nums:
    new_url = start_url + str(num)
    category(new_url)
