"""
"""
version = "0.0.7"
try:
    from rieapie.trickery import Api, pre_request,post_request
    import rieapie.wrappers
except ImportError as e:
    print("error initializing rieapie")
