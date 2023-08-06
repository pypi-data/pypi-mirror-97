class HttpRequest: 

    def __init__(self, 
                http_method, 
                query_url, 
                headers=None, 
                query_parameters=None,
                parameters=None, 
                cookies=None,  
                files=None):
                
        self.http_method = http_method 
        self.query_url = query_url 
        self.headers = headers 
        self.query_parameters = query_parameters 
        self.parameters = parameters 
        self.cookies = cookies
        self.files = files 
