from unittest import TestCase
import mock
import rieapie
import json

class TestPutPostDelete(TestCase):

    def test_root_put(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.put.return_value.text = json.dumps({'test':'ok'})
            api = rieapie.Api("http://nowhere.com")
            assert {'test':'ok'} == api.root.create()
            sess.return_value.put.assert_called_with(
                    "http://nowhere.com/", headers={}, data={}, params={}
                    )
    def test_root_post(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.post.return_value.text = json.dumps({'test':'ok'})
            api = rieapie.Api("http://nowhere.com")
            assert {'test':'ok'} == api.root.update(a=1,b=2)
            sess.return_value.post.assert_called_with(
                    "http://nowhere.com/", headers={}, data={"a":1,"b":2}, params={}
                    )
    def test_root_delete(self):
        with mock.patch("requests.Session") as sess:
            sess.return_value.delete.return_value.text = json.dumps({'test':'ok'})
            api = rieapie.Api("http://nowhere.com")
            assert {'test':'ok'} == api.root.delete(a=1,b=2)
            sess.return_value.delete.assert_called_with(
                    "http://nowhere.com/", headers={}, params={"a":1,"b":2}
                    )
