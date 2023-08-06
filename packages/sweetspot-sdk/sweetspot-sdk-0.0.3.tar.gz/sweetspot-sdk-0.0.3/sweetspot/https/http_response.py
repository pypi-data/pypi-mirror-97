class HttpResponse(object):

    def __init__(self, 
                status_code, 
                reason_phrase, 
                headers, 
                text, 
                cookies, 
                request):

        self.status_code = status_code 
        self.reason_phrase = reason_phrase 
        self.headers = headers 
        self.text = text 
        self.cookies = cookies.get_dict()
        self.request = request 
        