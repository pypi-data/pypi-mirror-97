import requests, json

class call:
    def __init__(self):
        pass

    def get(self, url, params):
        response = requests.get(url, params=params)
        tmp = None
        if response.status_code == 200:
            tmp = response.json()
        return tmp

    def post(self, url, params):
        response = requests.get(url, params=params)
        if response.json():
            return response.json()
        return None