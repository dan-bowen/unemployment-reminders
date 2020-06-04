"""
Main application package.
"""

from flask import Flask
from .config import get_config
from .extension import twilio_bot
from .blueprint import ping, twilio


def create_app():
    """
    An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    :return:
    """

    app = Flask(__name__)

    # load config for the environment
    config_object = get_config()

    # configure the app
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """
    Register Flask extensions.

    :param app:
    :return:
    """
    twilio_bot.init_app(app)


def register_blueprints(app):
    """
    Register Flask Blueprints.

    :param app:
    :return:
    """

    app.register_blueprint(ping.blueprint)
    app.register_blueprint(twilio.blueprint)
