import jsonpickle 
import re

class ApiHelper(object):

    @staticmethod
    def merge_dicts(dict1, dict2):
        temp = dict1.copy()
        temp.update(dict2)
        return temp

    @staticmethod
    def clean_url(url):
        regex = "^http?://[^/]+"
        match = re.match(regex, url)
        if match is None:
            raise ValueError('Invalid Url format.')

        protocol = match.group(0)
        index = url.find('?')
        query_url = url[len(protocol): index if index != -1 else None]
        query_url = re.sub("//+", "/", query_url)
        parameters = url[index:] if index != -1 else ""

        return protocol + query_url + parameters

    @staticmethod 
    def json_serialize(obj):
        return jsonpickle.encode(obj)

    @staticmethod 
    def json_deserialize(json):
        if not json: 
            return json 
        try:
            decoded = jsonpickle.decode(json)
            return decoded 
        except ValueError: 
            return json 



         
