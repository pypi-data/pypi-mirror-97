from copy import deepcopy

from sweetspot.https.http_client import HttpClient

class Configuration(object): 

	environments = {
		'development': 'http://app:5000/api',
		'production': 'http://sweetspot.so'
	}

	def __init__(self, csrf_access_token=None, 
				 csrf_refresh_token=None, 
				 access_token_cookie=None, 
				 refresh_token_cookie=None,
				 environment='development'):
		self.csrf_access_token = csrf_access_token
		self.csrf_refresh_token = csrf_refresh_token
		self.access_token_cookie = access_token_cookie 
		self.refresh_token_cookie = refresh_token_cookie
		self.environment = environment
		self.http_client = self.create_http_client()

	def get_base_uri(self):
		return self.environments[self.environment]

	def create_http_client(self):
		return HttpClient()

