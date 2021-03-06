import requests
import logging
import functools
import inspect
import json

GET = "GET"
PUT = "PUT"
POST = "POST"
DELETE = "DELETE"


class Component(object):
    def __init__(self, name, api_object, parent=None):
        self.name = str(name)
        self.parent = parent
        self.api_object = api_object

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return Component(key, self.api_object, self)

    def __full_path(self):
        return "/".join([self.api_object.base_url, self.__path()])

    def __path(self):
        path = []
        cur = self
        while cur.parent:
            path += [cur.name]
            cur = cur.parent
        path += [cur.name]
        return "/".join(reversed(path))

    def __repr__(self):
        return self.__path().replace("/", ".")

    def __call__(self, ext=""):
        if ext:
            return Component("%s.%s" % (self.name, ext), self.api_object,
                             self.parent)
        return self

    def __getitem__(self, key):
        return Component(key, self.api_object, self)

    def get(self, **kwargs):
        url, params, _, headers = self.api_object.execute_pre_request(
            GET, self.__full_path(), kwargs, None,
            self.api_object.headers)
        resp = self.api_object.session.get(url, params=params, headers=headers)
        return self.api_object.execute_post_request(resp.status_code,
                                                    resp.text)

    def delete(self, **kwargs):
        url, params, _, headers = self.api_object.execute_pre_request(
            DELETE, self.__full_path(), kwargs, None,
            self.api_object.headers)
        resp = self.api_object.session.delete(url, params=params,
                                              headers=headers)
        return self.api_object.execute_post_request(resp.status_code,
                                                    resp.text)

    def create(self, **kwargs):
        url, params, data, headers = self.api_object.execute_pre_request(
            PUT, self.__full_path(), {}, kwargs,
            self.api_object.headers)
        resp = self.api_object.session.put(url, params=params, data=data,
                                           headers=headers)
        return self.api_object.execute_post_request(resp.status_code,
                                                    resp.text)

    def update(self, **kwargs):
        url, params, data, headers = self.api_object.execute_pre_request(
            POST, self.__full_path(), {}, kwargs,
            self.api_object.headers)
        resp = self.api_object.session.post(url, params=params, data=data,
                                            headers=headers)
        return self.api_object.execute_post_request(resp.status_code,
                                                    resp.text)


def pre_request(fn):
    fn.is_pre_request = True

    @functools.wraps(fn)
    def __inner(*args, **kwargs):
        return fn(*args, **kwargs)

    return __inner


def post_request(fn):
    fn.is_post_request = True

    @functools.wraps(fn)
    def __inner(*args, **kwargs):
        return fn(*args, **kwargs)

    return __inner


class Api(object):
    def __init__(self, base_url, request_headers={}, debug=False, pool_size=10,
                 connect_timeout=5, response_timeout=10):
        self.base_url = base_url.rstrip("/")
        self.headers = request_headers
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        self.pre_request_chain = []
        self.post_request_chain = []
        for name, method in inspect.getmembers(self, inspect.ismethod):
            if hasattr(method, "is_pre_request"):
                self.pre_request_chain.append(method)
            if hasattr(method, "is_post_request"):
                self.post_request_chain.append(method)
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_maxsize=pool_size,
                                                max_retries=2)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.root = Component("", self, None)

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return Component(key, self, None)

    @pre_request
    def default_pre_request(self, method, url, params, data, headers):
        return url, params, data, headers

    @post_request
    def default_post_request(self, status, body):
        return json.loads(body)

    @post_request
    def fallback_post_request(self, status, body):
        return body

    def execute_pre_request(self, method, url, params, data, headers):
        for fn in self.pre_request_chain:
            url, params, data, headers = fn(method, url, params, data, headers)
        return url, params, data, headers

    def execute_post_request(self, status, body):
        last_error = None
        num_errors = 0
        for fn in self.post_request_chain:
            try:
                body = fn(status, body)
            except Exception as e:
                num_errors += 1
                last_error = e

        if num_errors == len(self.post_request_chain):
            raise last_error
        else:
            return body

