from bs4 import BeautifulSoup
import urllib.request
import codecs

from db.DataBase_Ulmart import DataBase_Ulmart


def parse_reviews(start_link):
    with urllib.request.urlopen(start_link) as url:
        html = url.read()
    soup = BeautifulSoup(html, "lxml")
    pages_finished = False
    page_num = 1
    while not pages_finished:
        new_url = start_link + str(page_num)
        page_num += 1
        for title in soup.findAll("div", {"class": "b-product__art"}):  # get all products
            article = title.find("span").text
            print(article)
            completed = False
            while not completed:
                try:
                    product(article)
                    completed = True
                except:
                    print("Error, try again!")


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


def parse_sub_category(start_link):
    with urllib.request.urlopen(start_link) as url:
        html = url.read()
    soup = BeautifulSoup(html, "lxml")
    for category in soup.findAll("div", {"class": "col-main-4"}):
        ul = category.find("ul")
        for li in ul.findAll("li", {"class": "b-list__item b-list__item_bigger "}):
            name = li.text
            name = name.replace("\n", "")
            link = start_url + li.find('a', href=True)['href']
            print("\t" + link + " " + name)
            parse_reviews(link)


def parse_categories():
    with codecs.open("category_links.txt", "r", "utf-8") as links:
        for link in links:
            parsed_link = link.partition(' ')[0]
            name = link.partition(' ')[2]
            name = name.replace("\n", "")
            print(parsed_link + " " + name)
            parse_sub_category(parsed_link)


dataBase = DataBase_Ulmart()
url_market = "https://www.ulmart.ru/"
start_url = "https://www.ulmart.ru/catalog/computers_notebooks"
parse_categories()
