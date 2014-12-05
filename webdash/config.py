mongouri='mongodb://localhost/webdash'
log_level='INFO'
log_path='./logs/webdash.log'

urls = []

try:
    from .config_local import *
except ImportError:
    pass
