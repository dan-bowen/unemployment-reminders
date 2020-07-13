"""
Main application package.
"""

from flask import Flask
from config import config
from .blueprint import bot


def create_app():
    """
    An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    :return:
    """

    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """
    Register Flask extensions.

    :param app:
    :return:
    """
    pass


def register_blueprints(app):
    """
    Register Flask Blueprints.

    :param app:
    :return:
    """
    app.register_blueprint(bot.blueprint)
