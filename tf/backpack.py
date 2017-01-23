import urllib.request
import urllib.parse
import json

__useragent__ =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

class RemoteJSONHandler:
    def __init__(self):
        pass
    def open_get(self, url, params, headers=None):
        if headers:
            data = urllib.parse.urlencode(params)
            print(url + '?' + data)
            req = urllib.request.Request(url + '?' + data, headers=headers)
        else:
            req = urllib.request.Request(url)
        opened = urllib.request.urlopen(req)
        result = json.loads(opened.read().decode('UTF-8'))
        return result

class Backpack(RemoteJSONHandler):
    def __init__(self, api, local = False):
        self.__api__ = api
        self.prices = {}
        self.currency = {}
        self.local = local
    
    def fetch_prices(self):
        if self.local:
            url = "file:prices.json"
            headers = None
            params = None
        else:
            url = "http://backpack.tf/api/IGetPrices/v4"
            headers = {
                'User-Agent': __useragent__
            }
            params = {
                "format" : "json",
                "key" : self.__api__,
                "appid" : 440
            }
        self.prices = RemoteJSONHandler.open_get(self, url, params, headers)
        return self.prices
    
    def get_prices(self):
        if not self.prices:
            self.fetch_prices()
        return self.prices
    
    def fetch_currency(self):
        url = "http://backpack.tf/api/IGetCurrencies/v1"
        headers = {
            'User-Agent': __useragent__
        }
        params = {
            "format" : "json",
            "key" : self.__api__,
            "appid" : 440
        }
        self.currency = RemoteJSONHandler.open_get(self, url, params, headers)
        return self.currency

class Steam(RemoteJSONHandler):
    def __init__(self, api):
        self.__api__ = api
        self.schema = {}

    def fetch_items(self, id):
        url = "http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/"
        headers = {
            'User-Agent': __useragent__
        }
        params = {
            "key" : self.__api__,
            "SteamID" : id
        }
        return RemoteJSONHandler.open_get(self, url, params, headers)

    def fetch_schema(self, local=False):
        url = "http://api.steampowered.com/IEconItems_440/GetSchema/v0001"
        headers = {
            'User-Agent': __useragent__
        }
        params = {
            "key": self.__api__,
            "language": "en_US"
        }
        self.schema = RemoteJSONHandler.open_get(self, url, params, headers)
        return self.schema

    def get_schema(self):
        if not self.schema:
            self.fetch_schema()
        return self.schema