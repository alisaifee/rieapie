.. |travis-ci| image:: https://secure.travis-ci.org/alisaifee/rieapie.png 
    :target: https://travis-ci.org/#!/alisaifee/rieapie 
.. |coverall| image:: https://coveralls.io/repos/alisaifee/rieapie/badge.png?branch=master
    :target: https://coveralls.io/r/alisaifee/rieapie

rieapie |travis-ci| |coverall| 
------------------------------

Introduction
============
An example for accessing google maps rest api using rieapie.

.. code-block:: python

    import rieapie 
    gmap = rieapie.Api("http://maps.googleapis.com/maps/api")
    args = {
     "origin"      : "Toronto"
    ,"destination" : "Montreal"
    ,"avoid"       : "highways"
    ,"mode"        : "bicycling"
    ,"sensor"      : "false"
    }
    directions = gmap.directions.json.get(**args)
    print directions["routes"][0]["bounds"]

An example for accessing the twitter api with the provided twitter wrapper.

.. code-block:: python

    import rieapie
    params = {
     "consumer_key"    : "..."
    ,"consumer_secret" : "..."
    }
    # or if you want to provide an access token
    params = {
     "consumer_key"        : "..."
    ,"consumer_secret"     : "..."
    ,"access_token"        : "..",
    ,"access_token_secret" : ".."
    }
    
    twitter = rieapie.wrappers.Twitter( **params )
    
    timeline = twitter.statuses.user_timeline(ext="json")
    # or if you prefer this syntax 
    timeline = twitter.statuses["user_timeline.json"]
    for status in timeline.get(count=10, screen_name="mybestfriend"):
        print status['text']


WTF is that name?
================= 
* [**R**]est [**i**]s [**E**]asy [**a**]s [**P**]ython [**i**]s [**E**]asy
* [**R**]est [**i**]s [**E**]asy [**a**]s [**PIE**]
* [**R**]est [**i**]s [**E**]asy [**API**]... [**E**]asy 
