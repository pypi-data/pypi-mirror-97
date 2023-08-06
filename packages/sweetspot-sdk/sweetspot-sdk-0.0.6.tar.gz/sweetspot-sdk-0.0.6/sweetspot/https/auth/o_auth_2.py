class OAuth2: 

    @staticmethod 
    def apply(config, http_request):
        csrf_access_token = config.csrf_access_token 
        access_token_cookie = config.access_token_cookie 
        http_request.headers['X-CSRF-TOKEN'] = csrf_access_token 
        http_request.cookies['access_token_cookie'] = access_token_cookie

    @staticmethod 
    def apply_refresh(config, http_request):
        csrf_refresh_token = config.csrf_refresh_token
        refresh_token_cookie = config.refresh_token_cookie 
        http_request.headers['X-CSRF-TOKEN'] = csrf_refresh_token 
        http_request.cookies['refresh_token_cookie'] = refresh_token_cookie

        
         

