import time

from db.DataBase import DataBase
from grab import Grab


def reviews():
    with open("reviewslinks.txt", "r") as links:
        for link in links:
            link = link.replace("\n", "")
            g.go(link)
            print(link)
            for i in g.doc.select('//div[@class="product-review-item product-review-item_collapsed_yes js-review"]'):
                if g.doc.select('//div[@class="product-review-item product-review-item_collapsed_yes js-review"]').exists():
                    review_dost = i.attr('href')
                    review_nedost = i.attr('href')
                    review_comment = i.attr('href')
                    dataBase.add_review("Компьютерная техника", "Компьютеры", "Подкатегория", 0,
                                        review_dost, review_nedost, review_comment,
                                        0)  # insert the review into data base


def model_info():
    with open("allproducts.txt", "r") as products, open("reviewslinks.txt", "w") as links:
        for product in products:
            time.sleep(3)
            product = product.replace("\n", "")
            g.go(product)
            print(product)
            link = g.doc.select('//a[@class="link n-smart-link i-bem"]/@href').node()
            links.write("https://market.yandex.ru" + link)
            links.write('\n')


def model_method():
    with open("allmodelsbuttonlinks.txt", "r") as links, open("allproducts.txt", "a") as products:
        for link in links:
            time.sleep(5)
            g.go(link)
            print(link)
            product = g.doc.select('//a[@class="snippet-card__image link"]/@href').node()
            products.write("https://market.yandex.ru" + product)
            products.write('\n')
    model_info()


def all_model_method():
    with open("catalogmodels.txt", "r") as catalogmodels, open("allmodelsbuttonlinks.txt", "w") as allmodelsbuttonlinks:
        for catalogmodel in catalogmodels:
            g.go(catalogmodel)
            all_button = g.doc.select('//div[@class="catalogmodels__more-models"]//h2//a/@href').node()
            allmodelsbuttonlinks.write("https://market.yandex.ru" + all_button)
            allmodelsbuttonlinks.write('\n')


def subcategory_method():
    with open('categories.txt', "r") as categories, open("catalogmodels.txt", "w") as catalogmodels:
        for category in categories:
            g.go(category)
            for i in g.doc.select('//a[@class="link catalog-menu__title metrika i-bem"]'):
                if g.doc.select('//a[@class="link catalog-menu__title metrika i-bem"]').exists():
                    catalogmodels.write("https://market.yandex.ru" + i.attr('href'))
                    catalogmodels.write('\n')
    all_model_method()


def category_method(url):
    with open('categories.txt', 'w') as categories:
        g.go(url)
        for i in g.doc.select('//a[@class="link catalog-menu__title metrika i-bem"]'):
            if g.doc.select('//a[@class="link catalog-menu__title metrika i-bem"]').exists():
                categories.write("https://market.yandex.ru" + i.attr('href'))
                categories.write('\n')
    subcategory_method()


g = Grab()
# url = 'https://market.yandex.ru/catalog/54425?hid=91009&track=menu'
# category_method(url)
# subcategory_method()
# all_model_method()
# model_method()
# model_info()
dataBase = DataBase()
reviews()
