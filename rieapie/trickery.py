import requests
import logging

GET = "GET"
PUT = "PUT"
POST = "POST"
DELETE = "DELETE"


class Component(object):
    def __init__(self, name, rieapie, parent=None):
        self.name = name
        self.parent = parent
        self.rieapie = rieapie

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except:
            return Component(key, self.rieapie, self)

    def full_path(self):
        return "/".join([self.rieapie.base_url, self.path()])

    def path(self):
        path = []
        cur = self
        while cur.parent:
            path += [cur.name]
            cur = cur.parent
        path += [cur.name]
        return "/".join(reversed(path))

    def __repr__(self):
        return self.path().replace("/", ".")

    def __call__(self, ext=""):
        if ext:
            self.name += ".%s" % ext
        return self

    def __getitem__(self, key):
        return Component(key, self.rieapie, self)

    def get(self, **kwargs):
        url, params, _, headers = self.rieapie.pre_request(GET, self.full_path(), kwargs, None, self.rieapie.headers)
        resp = requests.get(url, params=params, headers=headers)
        print resp.text
        return resp.json()

    def delete(self, **kwargs):
        url, params, _, headers = self.rieapie.pre_request(DELETE, self.full_path(), kwargs, None, self.rieapie.headers)
        resp = requests.delete(url, params=params, headers=headers)
        return resp.json()

    def create(self, **kwargs):
        url, params, data, headers = self.rieapie.pre_request(PUT, self.full_path(), {}, kwargs, self.rieapie.headers)
        resp = requests.put(url, params=params, data=data, headers=headers)
        return resp.json()

    def update(self, **kwargs):
        url, params, data, headers = self.rieapie.pre_request(POST, self.full_path(), {}, kwargs, self.rieapie.headers)
        resp = requests.post(url, params=params, data=data, headers=headers)
        return resp.json()


class Api(object):
    def __init__(self, base_url, request_headers={}, debug=False):
        self.base_url = base_url
        self.headers = request_headers
        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except:
            return Component(key, self, None)

    def pre_request(self, method, url, params, data, headers):
        return url, params, data, headers
