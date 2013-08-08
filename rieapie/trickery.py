import requests
import logging
import functools
import inspect

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
        url, params, _, headers = self.rieapie.execute_pre_request_chain(GET, self.full_path(), kwargs, None, self.rieapie.headers)
        resp = requests.get(url, params=params, headers=headers)
        print resp.text
        return resp.json()

    def delete(self, **kwargs):
        url, params, _, headers = self.rieapie.execute_pre_request_chain(DELETE, self.full_path(), kwargs, None, self.rieapie.headers)
        resp = requests.delete(url, params=params, headers=headers)
        return resp.json()

    def create(self, **kwargs):
        url, params, data, headers = self.rieapie.execute_pre_request_chain(PUT, self.full_path(), {}, kwargs, self.rieapie.headers)
        resp = requests.put(url, params=params, data=data, headers=headers)
        return resp.json()

    def update(self, **kwargs):
        url, params, data, headers = self.rieapie.execute_pre_request_chain(POST, self.full_path(), {}, kwargs, self.rieapie.headers)
        resp = requests.post(url, params=params, data=data, headers=headers)
        return resp.json()


def pre_request(fn):
    fn.is_pre_request = True

    @functools.wraps(fn)
    def __inner(*args, **kwargs):
        return fn(*args, **kwargs)
    return __inner


class Api(object):
    def __init__(self, base_url, request_headers={}, debug=False):
        self.base_url = base_url
        self.headers = request_headers
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        self.pre_request_chain = []
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "is_pre_request"):
                self.pre_request_chain.append(method)

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except:
            return Component(key, self, None)

    @pre_request
    def default_pre_request(self, method, url, params, data, headers):
        return url, params, data, headers

    def execute_pre_request_chain(self, method, url, params, data, headers):
        for fn in self.pre_request_chain:
            url, params, data, headers = fn(method, url, params, data, headers)
        return url, params, data, headers
