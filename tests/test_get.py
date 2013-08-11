from unittest import TestCase
import mock
import rieapie
import json

class TestGet(TestCase):

    def test_root_get(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = json.dumps({'test':'ok'})
            api = rieapie.Api("http://nowhere.com")
            assert {'test':'ok'} == api.root.get()
    def test_get_indexed(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = json.dumps({'test':'ok'})
            api = rieapie.Api("http://nowhere.com")
            assert {'test':'ok'} == api.res1[1]("json").get()
            sess.return_value.get.assert_called_with (
                    "http://nowhere.com/res1/1.json"
                    , headers = {}
                    , params = {}
                    )
    def test_get_non_json(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = "test"
            api = rieapie.Api("http://nowhere.com")
            assert "test" == api.res1[1]("json").get()
            sess.return_value.get.assert_called_with (
                    "http://nowhere.com/res1/1.json"
                    , headers = {}
                    , params = {}
                    )
    def test_hook_post_request(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = "test"
            class FooApi(rieapie.Api):
                @rieapie.post_request
                def parse(self, status, body):
                    return body[::-1]
            assert "tset" == FooApi("http://nowhere.com").res1.res2.get()
            sess.return_value.get.assert_called_with (
                    "http://nowhere.com/res1/res2"
                    , headers = {}
                    , params = {}
                    )

    def test_hook_pre_request(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = "test"
            class FooApi(rieapie.Api):
                @rieapie.pre_request
                def add_params(self, method, url, params, data, headers):
                    params = dict(params)
                    params["patch"] = True
                    return url, params, data, headers

                @rieapie.pre_request
                def add_header(self, method, url, params, data, headers):
                    headers = dict(headers)
                    headers["Accept"] = "application/json"
                    return url, params, data, headers

            assert "test" == FooApi("http://nowhere.com").res1.res2.get()
            sess.return_value.get.assert_called_with (
                    "http://nowhere.com/res1/res2"
                    , headers = {"Accept":"application/json"}
                    , params = {"patch":True}
                    )
    def test_get_params(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = "test"
            assert "test" == rieapie.Api("http://nowhere.com").res1.res2.get(a=1,b="test")
            sess.return_value.get.assert_called_with (
                    "http://nowhere.com/res1/res2"
                    , headers = {}
                    , params = {"a":1, "b":"test"}
                    )

