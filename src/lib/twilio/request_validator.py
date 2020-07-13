from urllib.parse import urlparse, urlunparse
from functools import wraps
from flask import abort, request, current_app
from lib.twilio import TwilioClient


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""

    # Adapted from https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-flask-app-by-validating-incoming-twilio-requests?code-sample=code-custom-decorator-for-flask-apps-to-validate-twilio-requests-3&code-language=Python&code-sdk-version=6.x
    @wraps(f)
    def decorated_function(*args, **kwargs):
        twilio_client = TwilioClient(
            current_app.config['SECRETS'].TWILIO_ACCOUNT_SID,
            current_app.config['SECRETS'].TWILIO_AUTH_TOKEN
        )

        # save variables from original request as we will be making transformations on it below
        original_url = request.url
        original_host_header = request.headers.get('X-Original-Host')

        # the url parts to be transformed
        twilio_url_parts = urlparse(original_url)

        """
        Solve issues with NGROK
        
        Twilio sees: http://somedomain.ngrok.io
        App sees:    http://localhost:5000
        
        So we replace the domain our app sees with the X-Original-Host header
        """
        if original_host_header:
            twilio_url_parts = twilio_url_parts._replace(netloc=original_host_header)

        """
        Solve issues with API Gateway custom domains
        
        Twilio sees: https://custom-domain.com/bot/validate-next-alert
        App sees:    https://custom-domain.com/{stage}/bot/validate-next-alert
        
        So we strip API_GATEWAY_BASE_PATH from the beginning of the path
        """
        api_gateway_base_path = current_app.config['API_GATEWAY_BASE_PATH']
        if api_gateway_base_path:
            # Strip N chars from beginning of path.
            chars_to_strip = len(f"/{api_gateway_base_path}")
            new_path = twilio_url_parts.path[chars_to_strip:]
            twilio_url_parts = twilio_url_parts._replace(path=new_path)

        # Validate the request using its URL, POST data, and X-TWILIO-SIGNATURE header
        request_valid = twilio_client.validate_request(
            urlunparse(twilio_url_parts), request.form, request.headers.get('X-TWILIO-SIGNATURE', '')
        )

        # Continue processing the request if it's valid, return a 403 error if it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_function
