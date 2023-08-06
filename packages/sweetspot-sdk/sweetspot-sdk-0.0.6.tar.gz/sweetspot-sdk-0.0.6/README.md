<p align="center"><img src="https://www.sweetspot.so/static/media/full-logo-white.png"></p>


# Sweetspot Python SDK

This Python library helps Sweetspot developers interact with their backend APIs to modify shops, merchants, and consumers.

## Installation 

```sh 
pip install sweetspot-sdk 
```

## Client 

The API client can be initialized as follows:

```python 
from sweetspot.client import Client 

client = Client(
    csrf_refresh_token='csrf_refresh_token', 
    csrf_access_token='csrf_access_token', 
    access_token_cookie='access_token_cookie', 
    refresh_token_cookie='refresh_token_cookie',
    environment='development')
```

API calls return an `ApiResponse` object that includes the following fields: 

| Field | Description |
|  --- | --- |
| `status_code` | Status code of the HTTP response |
| `reason_phrase` | Reason phrase of the HTTP response |
| `headers` | Headers of the HTTP response as a dictionary |
| `text` | The body of the HTTP response as a string |
| `request` | HTTP request info |
| `errors` | Errors, if they exist |
| `body` | The deserialized body of the HTTP response |
| `cookies` | The deserialized cookies of the HTTP response |


## Make Calls with the API Client 

```python 
from sweetspot.client import Client

client = Client(
    csrf_refresh_token='csrf_refresh_token', 
    csrf_access_token='csrf_access_token', 
    access_token_cookie='access_token_cookie', 
    refresh_token_cookie='refresh_token_cookie',
    environment='development')
    
category_result = client.category.get_all_categories()
if category_result.is_success():
    categories = category_result.body
```

## Authenticating the API Client 

The client must obtain access tokens and cookies in order to call protected endpoints.

```python 
from sweetspot.client import Client 

client = Client() 

login_payload = {
    'email':email,
    'password':password
}

authentication_result = client.authentication.get_authentication_information(login_payload)
if authentication_result.is_success(): 
    client.update_config(**authentication_result.cookies)

#call protected endpoint 

category_result = client.category.get_all_categories()
if category_result.is_success():
    categories = category_result.body
    
```








    
 
