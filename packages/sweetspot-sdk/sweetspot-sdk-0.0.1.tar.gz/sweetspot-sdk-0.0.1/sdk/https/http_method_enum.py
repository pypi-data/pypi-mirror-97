class HttpMethodEnum: 

    GET = "GET"

    POST = "POST"

    PUT = "PUT"

    PATCH = "PATCH"

    DELETE = "DELETE"

    @classmethod 
    def to_string(cls, val):
        for k, v in list(vars(cls).items()):
            if v == val: 
                return k 
                