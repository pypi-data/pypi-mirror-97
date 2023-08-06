import json


class ApiResponse:

    def __init__(self, http_response,
                 body=None,
                 errors=None):

        self.status_code = http_response.status_code
        self.reason_phrase = http_response.reason_phrase
        self.headers = http_response.headers
        self.text = http_response.text
        self.request = http_response.request
        self.cookies = http_response.cookies
        self.body = body
        self.errors = errors 

    @property 
    def errors(self):
        return self._errors 

    @errors.setter
    def errors(self, errors):
        if type(errors) in [dict, list]: 
            errors = self._parse_errors(errors)
        self._errors = errors

    def is_success(self):
        return 200 <= self.status_code < 300

    def is_error(self):
        return 400 <= self.status_code < 600

    def _parse_errors(self, errors):
        for key in errors: 
            curr = errors.get(key)
            if isinstance(curr, dict):
                return self._parse_errors(curr)
            elif isinstance(curr, list):
                return curr[0]
            else:
                return curr

    def __repr__(self):
        return f'<ApiResponse [{self.text}]>'