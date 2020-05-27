from urllib.parse import urlparse, urlunparse
from functools import wraps
from flask import abort, request, current_app
from lib.twilio import TwilioClient


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""

    # Adapted from https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-flask-app-by-validating-incoming-twilio-requests?code-sample=code-custom-decorator-for-flask-apps-to-validate-twilio-requests-3&code-language=Python&code-sdk-version=6.x
    @wraps(f)
    def decorated_function(*args, **kwargs):
        twilio_client = TwilioClient(current_app)

        # solve issues with NGROK
        url = request.url
        original_host = request.headers.get('X-Original-Host')
        if original_host:
            url_parts = urlparse(url)
            url = urlunparse(url_parts._replace(netloc=original_host))

        # Validate the request using its URL, POST data, and X-TWILIO-SIGNATURE header
        request_valid = twilio_client.validate_request(
            url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_function
