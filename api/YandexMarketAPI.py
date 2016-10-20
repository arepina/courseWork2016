import requests
import json


class YandexMarketAPI(object):
    API_VERSION = 1
    IP = '95.26.0.247'

    class NotAuthorized(BaseException):
        pass

    def __init__(self, key=None):
        if not key:
            raise YandexMarketAPI.NotAuthorized("You must provide authorization key to access Yandex.Market API!")
        self.key = key

    def errors(self, response, output):
        if response.status_code == 401:
            server_response = []
            for error in output['errors']:
                server_response.append(error)
            raise YandexMarketAPI.NotAuthorized(
                "Your key `%s' wasn't authorized at Yandex.Market API. Server response: %s" % (
                self.key, server_response))

    def make_url_categories(self, resource, format='json', version=API_VERSION, ip=IP):
        return 'https://api.content.market.yandex.ru/v%s/%s.%s?remote_ip=%s&fields=ALL&sort=NAME' % (version, resource, format, ip)

    def make_url_subcategories(self, cat_id, resource, format='json', version=API_VERSION, ip=IP):
        return 'https://api.content.market.yandex.ru/v%s/category/%s/%s.%s?remote_ip=%s&fields=ALL&sort=NAME' % (version, cat_id, resource, format, ip)

    def make_url_models(self, cat_id, resource, format='json', version=API_VERSION, ip=IP):
        return 'https://api.content.market.yandex.ru/v%s/category/%s/%s.%s?remote_ip=%s' % (version, cat_id, resource, format, ip)

    def make_url_reviews(self, model_id, resource, format='json', version=API_VERSION):
        return 'https://api.content.market.yandex.ru/v%s/model/%s/%s.%s?sort=rank' % (version, model_id, resource, format)

    def make_request_categories(self, resource, format='json', version=API_VERSION, params={}):
        url = self.make_url_categories(resource, format, version)
        params['Authorization'] = self.key

        response = requests.get(url, params=params, headers={'Authorization': self.key, 'Accept': '*/*'})
        output = json.loads(response.content.decode('utf-8'))
        print(output)

        self.errors(response, output)

        return output

    def make_request_subcategories(self, cat_id, resource, format='json', version=API_VERSION, params={}):
            url = self.make_url_subcategories(cat_id, resource, format, version)
            params['Authorization'] = self.key

            response = requests.get(url, params=params, headers={'Authorization': self.key, 'Accept': '*/*'})
            output = json.loads(response.content.decode('utf-8'))
            print(output)

            self.errors(response, output)

            return output

    def make_request_models(self, cat_id, resource, format='json', version=API_VERSION, params={}):
        url = self.make_url_models(cat_id, resource, format, version)
        params['Authorization'] = self.key

        response = requests.get(url, params=params, headers={'Authorization': self.key, 'Accept': '*/*'})
        output = json.loads(response.content.decode('utf-8'))
        print(output)

        self.errors(response, output)

        return output

    def make_model_reviews(self, model_id, resource, format='json', version=API_VERSION, params={}):
        url = self.make_url_reviews(model_id, resource, format, version)
        params['Authorization'] = self.key

        response = requests.get(url, params=params, headers={'Authorization': self.key, 'Accept': '*/*'})
        output = json.loads(response.content.decode('utf-8'))
        print(output)

        self.errors(response, output)

        return output

    def category(self):
        return self.make_request_categories('category')

    def subcategory(self, cat_id):
        return self.make_request_subcategories(cat_id, 'children')

    def model(self, cat_id):
        return self.make_request_models(cat_id, 'models')

    def model_review(self, model_id):
        return self.make_model_reviews(model_id, 'opinion')