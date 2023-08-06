class BaseApi(object):

    def __init__(self, config):
        self._config = config 

    @property 
    def config(self):
        return self._config 

    def validate_parameters(self, **kwargs):
        for name, value in kwargs.items():
            if not value: 
                raise ValueError(f"Required parameter {name} cannot be None")

    def execute_request(self, request):
        func = self.config.http_client.execute
        response = func(request)

        return response 

        
