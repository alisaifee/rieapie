"""
"""
version = "0.0.6.1"
try:
    from rieapie.trickery import Api, pre_request,post_request
    import rieapie.wrappers
except ImportError,e:
    print("error initializing rieapie")
