import rieapie
import urllib
import base64
import requests
class Twitter(rieapie.Api):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = "https://api.twitter.com/1.1"
        bearer_token = self.obtain_bearer_token()
        headers = {"Authorization":"Bearer %s" % bearer_token}
        rieapie.Api.__init__(self
                                , self.base_url
                                , request_headers = headers)
    def obtain_bearer_token(self):
        """
        request for an access token from twitter
        """
        _e_key = urllib.quote(self.consumer_key)
        _e_secret = urllib.quote(self.consumer_secret)
        credentials = base64.b64encode("%s:%s" % ( _e_key, _e_secret ))
        resp = requests.post("https://api.twitter.com/oauth2/token"
                , params = {"grant_type":"client_credentials"}
                , headers = {"Authorization": "Basic %s" % credentials} )
        resp_json = resp.json()
        if not resp_json.has_key("access_token"):
            raise UserWarning("failed to obtain access token : %s" % resp_json["errors"])
        return resp.json()["access_token"]

