import time
from bs4 import BeautifulSoup
import urllib.request


def category_method(html, start_link):
    time.sleep(7)
    soup = BeautifulSoup(html, "lxml")
    if start_link.startswith("/catalogmodels.xml"):  # look through the models page
        more_models = soup.find("div", {"class": "catalogmodels__more-models"})  # find the get all models href
        more_models_link = more_models.find('h2').find('a', href=True)['href']
        more_models_name = more_models.find('h2').text
        print(more_models_link + " " + more_models_name)
        with urllib.request.urlopen(url_market + more_models_link) as url:
            sub_category_html = url.read()
        category_method(sub_category_html, more_models_link)  # get all models for each category
    elif start_link.startswith("/guru.xml"):  # look through the models list
        for review_object in soup.findAll("div", {"class": "snippet-card__menu-item"}):  # find the product review link
            reviews_link = review_object.find('a', href=True)['href']
            print(reviews_link)
            with urllib.request.urlopen(url_market + reviews_link) as url:
                sub_category_html = url.read()
            category_method(sub_category_html, reviews_link)  # get all reviews for each product
    elif start_link.startswith("/product.xml"):  # get the reviews
        print("hello")
    else:
        for category in soup.findAll("div", {"class": "catalog-menu__item"}):  # get all categories from html file
            category_link = category.find('a', href=True)['href']
            category_name = category.text
            print(category_link + " " + category_name)
            with urllib.request.urlopen(url_market + category_link) as url:
                sub_category_html = url.read()
            category_method(sub_category_html, category_link)  # get all subcategories for each category


url_market = "https://market.yandex.ru"
start_url = "https://market.yandex.ru/catalog/54425?hid=91009&track=menu"  # the page we get categories from
with urllib.request.urlopen(start_url) as url:
    market_html = url.read()
category_method(market_html, start_url)
