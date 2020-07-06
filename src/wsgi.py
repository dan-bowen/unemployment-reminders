"""
Module for serverless wsgi

Simply exports the Flask WSGI app.
"""
from api import create_app

app = create_app()
