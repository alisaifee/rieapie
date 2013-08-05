import urllib
import requests
import json

class Component(object):
    def __init__(self, name, rieapie, parent=None):
        self.name = name
        self.parent = parent
        self.rieapie = rieapie

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self,key)
        except:
            return Component(key, self.rieapie, self)

    def full_path(self):
        return "/".join([self.rieapie.base_url, self.path()])

    def path(self):
        path = []
        cur = self
        while cur.parent:
            path+=[cur.name]
            cur = cur.parent
        path += [cur.name]
        return "/".join(reversed(path))

    def __repr__(self):
        return self.path().replace("/",".")

    def __call__(self, ext=""):
        if ext:
            self.name += ".%s" % ext
        return self

    def __getitem__(self, key):
        return Component(key, self.rieapie, self)

    def get(self,  **kwargs):
        url = self.full_path() + "?" + urllib.urlencode(kwargs)
        resp = requests.get( self.rieapie.pre_request(url) )
        return resp.json()

    def delete(self, **kwargs):
        url = self.full_path()+"?"+urllib.urlencode(kwargs)
        resp = requests.delete( self.rieapie.pre_request(url, kwargs))
        return resp.json()

    def create(self, **kwargs):
        raise NotImplementedError()

    def update(self, **kwargs):
        url = self.full_path()+"?"
        resp = requests.post( self.rieapie.pre_request(url, kwargs), data=json.dumps(kwargs))
        return resp.json()


class Rieapie(object):
    def __init__(self, base_url):
        self.base_url = base_url
    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self,key)
        except:
            return Component(key, self, None)

    def pre_request(self, url, payload):
        return url
