from webapi import WebApiCall
import json


class _JSONParseCall:

    def __init__(self, method):
        self.method = method

    def __call__(self, **kwargs):
        return json.loads(self.method(**kwargs), "UTF-8")


class Backpack:

    def __init__(self, host, port, api):
        self._api = api
        self.get_prices = _JSONParseCall(WebApiCall(
            method_name="backpack_get_prices", 
            host=host, 
            port=port, 
            key=self._api)
        )


class Steam:

    def __init__(self, host, port, api):
        self._api = api
        self.get_schema = _JSONParseCall(WebApiCall(
            method_name="steam_get_schema", host=host, port=port, key=api))
        self.get_items = _JSONParseCall(WebApiCall(
            method_name="steam_get_items", host=host, port=port, key=api))
