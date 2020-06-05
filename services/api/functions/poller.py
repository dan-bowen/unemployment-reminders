from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
# TODO Not thrilled with this hack. Find a better way to let python know about our packages
# TODO Imports in general are a little messy. Clean up app-wide
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

from api.wsgi import app


def lambda_handler(event, context):
    return {'bot_base_url': app.config['BOT_BASE_URL']}
