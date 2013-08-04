rieapie
-------

Introduction
============
Random example for accessing a rest api using rieapie.

.. code-block:: python

    import rieapie 
    gmap = rieapie.Rieapie("http://maps.googleapis.com/maps/api")
    directions = gmap.directions.json.get(origin="Toronto",destination="Montreal", avoid="highways", mode="bicycling", sensor="false")
    print directions["routes"][0]["bounds"]

WTF is that name?
================= 
* [**R**]est [**i**]s [**E**]asy [**a**]s [**P**]ython [**i**]s [**E**]asy
* [**R**]est [**i**]s [**E**]asy [**a**]s [**PIE**]
* [**R**]est [**i**]s [**E**]asy [**API**]... [**E**]asy 
