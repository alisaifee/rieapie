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
    def test_get_non_json(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = "test"
            api = rieapie.Api("http://nowhere.com")
            assert "test" == api.res1[1]("json").get()
    def test_hook_post_request(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.get.return_value.text = "test"
            class FooApi(rieapie.Api):
                @rieapie.post_request
                def parse(self, status, body):
                    return body[::-1]
            print FooApi("http://nowhere.com").res1.res2.get()

