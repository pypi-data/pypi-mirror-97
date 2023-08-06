from functools import lru_cache

from .configuration import Configuration
from .decorators import cached_property
from .apis.beta_user_api import BetaUserApi
from .apis.authentication_api import AuthenticationApi
from .apis.merchant_api import MerchantApi
from .apis.shop_api import ShopApi
from .apis.option_api import OptionApi 
from .apis.item_api import ItemApi
from .apis.modifier_api import ModifierApi
from .apis.category_api import CategoryApi

class Client: 

    def __init__(self, csrf_acccess_token=None, 
                 csrf_refresh_token=None, 
                 access_token_cookie=None, 
                 refresh_token_cookie=None,
                 environment='development', 
                 config=None):
        if config: 
            self.config = config 
        else:
            self.config = Configuration(
                csrf_access_token=csrf_acccess_token, 
                csrf_refresh_token=csrf_refresh_token,
                access_token_cookie=access_token_cookie, 
                refresh_token_cookie=refresh_token_cookie,
                environment=environment)

    def update_config(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self.config, k):
                setattr(self.config, k, v)
                
    @cached_property
    def beta_user(self):
    	return BetaUserApi(self.config)

    @cached_property 
    def authentication(self):
        return AuthenticationApi(self.config)

    @cached_property 
    def merchant(self):
        return MerchantApi(self.config)

    @cached_property 
    def shop(self):
        return ShopApi(self.config)

    @cached_property 
    def category(self):
        return CategoryApi(self.config)

    @cached_property 
    def modifier(self):
        return ModifierApi(self.config)

    @cached_property 
    def item(self):
        return ItemApi(self.config)

    @cached_property 
    def option(self):
        return OptionApi(self.config)


                


