import urllib
import requests

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
        return self.name

    def __call__(self, ext=""):
        if ext:
            self.name += ".%s" % ext
        return self

    def get(self, **kwargs):
        url = self.full_path() + "?" + urllib.urlencode(kwargs)
        return requests.get( self.rieapie.pre_request(url) ).json()

    def delete(self, **kwargs):
        raise NotImplementedError()

    def create(self, **kwargs):
        raise NotImplementedError()

    def update(self, **kwargs):
        raise NotImplementedError()


class Rieapie(object):
    def __init__(self, base_url):
        self.base_url = base_url
    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self,key)
        except:
            return Component(key, self, None)

    def pre_request(self, url):
        return url
