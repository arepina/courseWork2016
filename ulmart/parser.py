from bs4 import BeautifulSoup
import urllib.request
import codecs

from db.DataBase_Ulmart import DataBase_Ulmart


def parse_product(start_link, category_name, subcategory_name):
    with urllib.request.urlopen(start_link) as url:
        html = url.read()
    soup = BeautifulSoup(html, "lxml")
    products_num = soup.find("span", {"class": "text-sm text-muted"}).findAll("span")[1].text  # get the products number
    if int(products_num) <= 30:  # count the pages number (30 items per page)
        pages_num = 1
    else:
        pages_num = round(int(products_num) / 30)
    nums = [x for x in range(1, pages_num)]
    last_slash_num = start_link.rfind("/")
    review_url = "https://www.ulmart.ru/catalogAdditional" + start_link[last_slash_num:] + "?pageNum="
    for num in nums:  # look through all pages with products kept on page with start_link
        new_url = review_url + str(num)
        with urllib.request.urlopen(new_url) as url:  # load products for a concrete page
            html = url.read()
        soup = BeautifulSoup(html, "lxml")
        all_products = soup.findAll("div", {"class": "b-product__art"})
        for title in all_products:  # look through all products on a concrete page
            article = title.find("span").text
            print("\t\t" + article)
            completed = False
            while not completed:  # get the reviews for each product item with unique article
                try:
                    reviews(article, category_name, subcategory_name)
                    completed = True
                except Exception as e:  # there was an error during the reviews parsing
                    print(str(e))


def reviews(article, category_name, subcategory_name):
    reviews_url = "https://www.ulmart.ru/goods/" + article + "/reviews"  # generate the url for the concrete product
    with urllib.request.urlopen(reviews_url) as url:
        html = url.read()
    soup = BeautifulSoup(html, "lxml")
    reviews_num_already_have = dataBase.reviews_num(
        article)  # check if we have already loaded the reviews in our data base
    if reviews_num_already_have is not None:
        reviews_num_already_have = reviews_num_already_have[0]  # we have
    else:
        reviews_num_already_have = 0  # we have not
    try:
        all_reviews_num = soup.find("div", {
            "class": "b-stars-wrap b-stars-wrap_theme_normal _big"}).find("span").find(
            "span").text  # get all reviews number
    except Exception as e:  # there was an error during the reviews parsing
        print(str(e))
        return  # case when there are no reviews at all for the product, so they can not be found
    if int(all_reviews_num) <= 10:  # calculate the number of pages we have for reviews
        reviews_pages_num = 1
    else:
        reviews_pages_num = round(int(all_reviews_num) / 10)
    if reviews_num_already_have == int(all_reviews_num):  # we have already downloaded all the reviews for this product
        return
    if reviews_num_already_have != 0:
        dataBase.remove_review(article)  # remove the unfinished product reviews to start filing it again
    nums = [x for x in range(1, reviews_pages_num + 1)]
    for num in nums:  # look through all pages with products kept on page with start_link
        full_url = reviews_url + "/" + str(num)  # generate the full url for each reviews page
        with urllib.request.urlopen(full_url) as url:  # load products for a concrete page
            html = url.read()
        soup = BeautifulSoup(html, "lxml")
        reviews_on_page = soup.findAll("ul", {"class": "b-list b-list_theme_normal b-list_title-left b-list_review"})
        for review in reviews_on_page:  # get all reviews from concrete product on concrete page
            adv = 'Null'
            dis = 'Null'
            com = 'Null'
            for review_part in review.findAll("li", {"class": "b-list__item"}):  # parse the review parts
                name = review_part.find('span').text
                if name == "Достоинства":
                    adv = review_part.find('div').text
                elif name == "Недостатки":
                    dis = review_part.find('div').text
                elif name == "Общие впечатления":
                    com = review_part.find('div').text
            dataBase.add_review(category_name, subcategory_name, article, adv, dis,
                                com)  # add the review to the data base


def parse_sub_category(start_link, category_name):
    with urllib.request.urlopen(start_link) as url:
        html = url.read()
    soup = BeautifulSoup(html, "lxml")
    for category in soup.findAll("div", {"class": "col-main-4"}):  # all subcategories for category from start_link
        ul = category.find("ul")
        for li in ul.findAll("li", {"class": "b-list__item b-list__item_bigger "}):
            name = li.text
            name = name.replace("\n", "")
            link = url_market + li.find('a', href=True)['href']
            print("\t" + link + " " + name)
            parse_product(link, category_name, name)  # get all products for each subcategory


def parse_categories():
    with codecs.open("category_links.txt", "r", "utf-8") as links:  # all category links (they were downloaded before)
        for link in links:
            parsed_link = link.partition(' ')[0]
            name = link.partition(' ')[2]
            name = name.replace("\n", "")
            print(parsed_link + " " + name)
            parse_sub_category(parsed_link, name)  # get subcategories for each category


dataBase = DataBase_Ulmart()
url_market = "https://www.ulmart.ru/"
start_url = "https://www.ulmart.ru/catalog/computers_notebooks"
parse_categories()  # get categories
