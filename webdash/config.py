mongouri='mongodb://localhost/webdash'
urls = []

try:
    from .config_local import *
except ImportError:
    pass
