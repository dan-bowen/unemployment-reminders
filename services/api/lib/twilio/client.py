from twilio.request_validator import RequestValidator


class TwilioClient:
    def __init__(self, twilio_auth_token=None):
        self.request_validator = RequestValidator(twilio_auth_token)

    def compute_signature(self, uri, params):
        """proxy twilio.RequestValidator.compute_signature()"""
        return self.request_validator.compute_signature(uri, params)

    def validate_request(self, uri, params, signature):
        """proxy twilio.RequestValidator.validate()"""
        return self.request_validator.validate(uri, params, signature)
