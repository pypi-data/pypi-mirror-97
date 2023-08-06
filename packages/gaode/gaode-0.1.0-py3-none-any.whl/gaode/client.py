import requests
import json


class Gaode(object):
    def __init__(self, token):
        self.base_url = 'https://restapi.amap.com/v3/'
        self.token = token

    def get(self, path, payload):
        url = self.base_url + path
        payload.update({'key': self.token})
        response = requests.get(url, params=payload)
        return response.json()

    def place_text(self, keywords, types=None, city=None, citylimit=False, children=0, page=1, extensions='base'):
        return self.get('place/text', {'keywords': keywords})


if __name__ == '__main__':
    t = Gaode('377132d878695a67d528ba75f5a3200b')
    ret = t.place_text('饸饹')
    print(json.dumps(ret, indent=4, sort_keys=True))
