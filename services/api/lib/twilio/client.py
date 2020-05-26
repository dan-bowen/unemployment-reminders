import urllib
from twilio.request_validator import RequestValidator


class TwilioClient:
    def __init__(self, app=None):
        self.app = app
        # set by init_app()
        self.request_validator = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.request_validator = RequestValidator(app.config['SECRETS'].TWILIO_AUTH_TOKEN)

    def compute_signature(self, method, uri, params):
        """proxy twilio.RequestValidator.compute_signature()"""
        if method == "GET":
            uri = uri + '?' + urllib.parse.urlencode(params)
            params = {}
        return self.request_validator.compute_signature(uri, params)

    def validate_request(self, uri, params, signature):
        """proxy twilio.RequestValidator.validate()"""
        return self.request_validator.validate(uri, params, signature)
