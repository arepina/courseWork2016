from api.YandexMarketAPI import YandexMarketAPI
from db.DataBase import DataBase
from main.Category import Category
from main.Review import Review

dataBase = DataBase()
market = YandexMarketAPI('jIEfFMJdxnhBi5yQfJ0yMIPiKDnvUi')
categoriesList = market.category()['categories']  # all market categories (10 items)
for item in categoriesList['items']:
    if item['name'] == 'Компьютерная техника':
        category = Category(item['name'], item['parentId'], item['uniqName'], item['offersNum'], item['visual'],
                            item['modelsNum'], item['childrenCount'], item['type'], item['advertisingModel'],
                            item['link'], item['id'])
        subcategoriesList = market.subcategory(category.id)['categories']  # all 'computer technique' subcategories (10 items)
        for subItem in subcategoriesList['items']:
            if subItem['name'] == 'Компьютеры':
                subcategory = Category(subItem['name'], subItem['parentId'], subItem['uniqName'], subItem['offersNum'],
                                       subItem['visual'],
                                       subItem['modelsNum'], subItem['childrenCount'], subItem['type'],
                                       subItem['advertisingModel'],
                                       subItem['link'], subItem['id'])
                computerCategoriesList = market.subcategory(subcategory.id)[
                    'categories']  # all 'computer' subcategories (6 items)
                for computerItem in computerCategoriesList['items']:
                    modelsList = market.model(computerItem['id'])[
                        'models']  # get the model list of each computer subcategory
                    if modelsList['count'] != 0:
                        for modelItem in modelsList['items']:
                            reviews = market.model_review(modelItem['id'])[
                                'modelOpinions']  # get the review list of each model
                            for reviewItem in reviews['opinion']:
                                proItem = 'NULL'
                                textItem = 'NULL'
                                try:
                                    if 'pro' in reviewItem:
                                        proItem = reviewItem['pro']
                                except SyntaxError:
                                    pass
                                try:
                                    if 'text' in reviewItem:
                                        textItem = reviewItem['text']
                                except SyntaxError:
                                    pass
                                review = Review(proItem, textItem, reviewItem['id'],
                                                reviewItem['agree'], reviewItem['grade'], reviewItem['visibility'],
                                                reviewItem['anonymous'], reviewItem['date'],
                                                reviewItem['reject'], reviewItem['usageTime'])
                                print(modelItem['name'] + " " + str(review.id))
                                dataBase.add_review("Компьютерная техника", "Компьютеры", modelItem['name'], review.id,
                                                    review.pro, review.text, review.agree,
                                                    review.date)  # insert the review into data base