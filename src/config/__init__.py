from .config import get_config

"""
export config singleton

for now, this offers defense against calling the Secrets Manager API every time we need a config object
"""
config = get_config()
