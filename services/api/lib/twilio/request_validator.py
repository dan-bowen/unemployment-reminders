from flask import abort, request, current_app
from functools import wraps
from lib.twilio import TwilioClient


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        twilio_client = TwilioClient(current_app)

        # Validate the request using its URL, POST data, and X-TWILIO-SIGNATURE header
        request_valid = twilio_client.validate_request(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function
