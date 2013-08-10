import rieapie
import urllib
import base64
import requests
import time
import os
import hashlib
import hmac


class Twitter(rieapie.Api):
    def __init__(self, consumer_key, consumer_secret, access_token=None, access_token_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.base_url = "https://api.twitter.com/1.1"
        rieapie.Api.__init__(self, self.base_url)

    def obtain_bearer_token(self):
        """
        request for an access token from twitter
        """
        _e_key = urllib.quote(self.consumer_key)
        _e_secret = urllib.quote(self.consumer_secret)
        credentials = base64.b64encode("%s:%s" % (_e_key, _e_secret))
        resp = requests.post("https://api.twitter.com/oauth2/token"
                , params={"grant_type": "client_credentials"}
                , headers={"Authorization": "Basic %s" % credentials})
        resp_json = resp.json()
        if not resp_json.has_key("access_token"):
            raise UserWarning("failed to obtain access token : %s" % resp_json["errors"])
        return resp.json()["access_token"]

    @rieapie.pre_request
    def sign(self, method, url, params, data, headers):
        if not (self.access_token and self.access_token_secret):
            headers = {"Authorization": "Bearer %s" % self.obtain_bearer_token()}
        else:
            timestamp = int(time.time())
            consumer_key = self.consumer_key
            nonce = base64.binascii.b2a_hex(bytearray(os.urandom(16)))
            sig_params = dict(params)
            sig_params.update({
                "oauth_consumer_key": consumer_key
                , "oauth_nonce": nonce
                , "oauth_signature_method": "HMAC-SHA1"
                , "oauth_token": self.access_token
                , "oauth_timestamp": timestamp
                , "oauth_version": "1.0"
                })
            sig_pairs = []
            for key in sorted(sig_params.keys()):
                sig_pairs.append(urllib.quote_plus("%s=%s" % (key, str(sig_params[key]))))

            sig_string = "%s&%s&%s" % (method, urllib.quote_plus(url), urllib.quote("&").join(sig_pairs))
            signing_key = self.consumer_secret + "&" + self.access_token_secret
            hhmac = hmac.new(signing_key, digestmod=hashlib.sha1)
            hhmac.update(sig_string)
            sig = urllib.quote_plus(base64.b64encode(hhmac.digest()))
            token = self.access_token
            auth_string = """OAuth oauth_consumer_key="%(consumer_key)s",
            oauth_nonce="%(nonce)s",
            oauth_signature="%(sig)s",
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp="%(timestamp)d",
            oauth_token="%(token)s",
            oauth_version="1.0" """ % locals()
            headers = {"Authorization": auth_string}
        return url, params, data, headers
