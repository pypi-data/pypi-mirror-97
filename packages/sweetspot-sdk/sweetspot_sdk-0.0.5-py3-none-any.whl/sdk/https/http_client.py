import requests

from .http_method_enum import HttpMethodEnum
from .http_response import HttpResponse
from .http_request import HttpRequest 

class HttpClient: 

    def __init__(self):
        self.session = requests.session()

    def execute(self, request):
        response = self.session.request(
            HttpMethodEnum.to_string(request.http_method),
            request.query_url, 
            headers=request.headers,
            params=request.query_parameters,
            data=request.parameters, 
            cookies=request.cookies,
            files=request.files)

        return self.convert_response(response, request)

    def convert_response(self, response, http_request):
        return HttpResponse(response.status_code,
                            response.reason, 
                            response.headers,
                            response.text, 
                            response.cookies, 
                            http_request)
    
    def get(self, query_url, 
            query_parameters={},
            headers={},
            parameters={},
            cookies={},
            files={}):

        return HttpRequest(
            HttpMethodEnum.GET, 
            query_url,
            headers,
            query_parameters, 
            parameters, 
            cookies,
            files)

    def post(self, query_url, 
            query_parameters={},
            headers={},
            parameters={},
            cookies={},
            files={}):

        return HttpRequest(
            HttpMethodEnum.POST,
            query_url, 
            headers,
            query_parameters, 
            parameters, 
            cookies,
            files)

    def put(self, query_url, 
            headers={},
            query_parameters={},
            parameters={},
            cookies={},
            files={}):

        return HttpRequest(
            HttpMethodEnum.PUT,
            query_url, 
            headers,
            query_parameters, 
            parameters, 
            cookies,
            files)

    def patch(self, query_url, 
            headers={},
            query_parameters={},
            parameters={},
            cookies={},
            files={}):

        return HttpRequest(
            HttpMethodEnum.PATCH,
            query_url, 
            headers,
            query_parameters, 
            parameters, 
            cookies,
            files)

    def delete(self, query_url, 
            query_parameters={},
            headers={},
            parameters={},
            cookies={},
            files={}):

        return HttpRequest(
            HttpMethodEnum.DELETE, 
            query_url,
            headers,
            query_parameters, 
            parameters, 
            cookies,
            files)