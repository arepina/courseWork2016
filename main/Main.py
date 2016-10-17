from api.YandexMarketAPI import YandexMarketAPI
from main.Category import Category

market = YandexMarketAPI('jIEfFMJdxnhBi5yQfJ0yMIPiKDnvUi')
categoriesList = market.category()['categories']  # all market categories
for item in categoriesList['items']:
    if item['name'] == 'Компьютерная техника':
        category = Category(item['name'], item['parentId'], item['uniqName'], item['offersNum'], item['visual'],
                            item['modelsNum'], item['childrenCount'], item['type'], item['advertisingModel'],
                            item['link'], item['id'])
        subcategoriesList = market.subcategory(category.id)['categories']  # all computer technique subcategories
        for subItem in subcategoriesList['items']:
            if subItem['name'] == 'Компьютеры':
                subcategory = Category(subItem['name'], subItem['parentId'], subItem['uniqName'], subItem['offersNum'],
                                       subItem['visual'],
                                       subItem['modelsNum'], subItem['childrenCount'], subItem['type'],
                                       subItem['advertisingModel'],
                                       subItem['link'], subItem['id'])
                computerCategoriesList = market.subcategory(subcategory.id)['categories']  # all computer subcategories
                for computerItem in computerCategoriesList['items']:
                    modelsList = market.model(computerItem['id'])['models']  # get the model list of each computer subcategory
                    if modelsList['count'] != 0:
                        for modelItem in modelsList['items']:
                            reviews = market.model_review(modelItem['id'])['modelOpinions']  # get the review list of each model
