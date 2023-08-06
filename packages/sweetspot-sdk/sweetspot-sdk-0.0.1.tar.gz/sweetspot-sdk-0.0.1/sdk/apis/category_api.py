from .base_api import BaseApi 
from ..https.api_response import ApiResponse 
from ..https.auth.o_auth_2 import OAuth2 
from ..api_helper import ApiHelper 

class CategoryApi(BaseApi):

    def __init__(self, config):
        super().__init__(config)

    def get_all_categories(self):
        _url_path = f'/category'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path 
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = { 
            'accept': 'application/json'
        }

        _request = self.config.http_client.get(_query_builder, headers=_headers) 
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict: 
            _errors = decoded.get('error')
        else:
            _errors = None

        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result

    def add_category(self, payload):
        _url_path = f'/category'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = ApiHelper.clean_url(_query_builder)
        
        _headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8'
        }

        _request = self.config.http_client.post(_query_builder, headers=_headers, parameters=ApiHelper.json_serialize(payload))
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict: 
            _errors = decoded.get('error')
        else: 
            _errors = None
        
        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result 

    
