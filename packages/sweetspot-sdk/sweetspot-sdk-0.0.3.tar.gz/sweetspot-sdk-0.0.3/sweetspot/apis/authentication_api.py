from .base_api import BaseApi 
from ..https.api_response import ApiResponse 
from ..api_helper import ApiHelper 
from ..https.auth.o_auth_2 import OAuth2

class AuthenticationApi(BaseApi):

    def __init__(self, config):
        super().__init__(config)

    def get_authentication_information(self, payload):
        _url_path = '/authentication/login'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path 
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8'
        }

        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=ApiHelper.json_serialize(payload))
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict: 
            _errors = decoded.get('error')
        else:
            _errors = None

        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result 

    def refresh_access(self):
        _url_path = '/authentication/refresh-token'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path 
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = {
            'accept': 'application/json'
        }

        _request = self.config.http_client.post(_query_url, headers=_headers)
        OAuth2.apply_refresh(self.config, _request)
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict:   
            _errors = decoded.get('error')
        else:
            _error = None 
        
        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result

    def unset_access(self):
        _url_path = '/authentication/logout'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = {
            'accept': 'application/json'
        }

        _request = self.config.http_client.post(_query_url, headers=_headers) 
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict: 
            _errors = deocded.get('error')
        else:
            _errors = None 
        
        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result 

    def send_verification_email(self, merchant_id):
        _url_path = f'/authentication/verify-email/{merchant_id}'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path 
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = {
            'accept': 'application/json'
        }

        _request = self.config.http_client.post(_query_url, headers=_headers)
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text) 
        if type(decoded) == dict: 
            _errors = decoded.get('error')
        else:
            _errors = None 

        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result

    def verify_email_token(self, payload):
        _url_path = f'/authentication/verify-email-token'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path 
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = { 
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }    

        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=ApiHelper.json_serialize(payload))
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)  

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict: 
            _errors = decoded.get('error')
        else:
            _errors = None 

        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result 

    def change_password(self, payload):
        _url_path = f'/authentication/change-password'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path 
        _query_url = ApiHelper.clean_url(_query_builder)

        _headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=ApiHelper.json_serialize(payload))
        OAuth2.apply(self.config, _request)
        _response = self.execute_request(_request)

        decoded = ApiHelper.json_deserialize(_response.text)
        if type(decoded) == dict: 
            _errors = decoded.get('error')
        else:
            _errors = None 

        _result = ApiResponse(_response, body=decoded, errors=_errors)
        return _result

        