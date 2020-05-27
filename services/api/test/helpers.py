from api import create_app
from lib.twilio import TwilioClient


class Helper:
    def __init__(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.twilio_client = TwilioClient(self.app)

    def twilio_request(self, method, path, params, valid=True):
        """
        Send a Twilio request with the test client

        valid=False forces an invalid signature

        Adapted from https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-flask-app-by-validating-incoming-twilio-requests?code-sample=code-test-the-validity-of-your-webhook-signature-3&code-language=Python&code-sdk-version=default
        """
        base_url = 'http://localhost'
        full_url = f'{base_url}{path}' if valid else f'{base_url}{path}/invalid'
        methods = {
            'GET': self.client.get,
            'POST': self.client.post
        }

        signature = self.twilio_client.compute_signature(full_url, params)

        headers = {'X-Twilio-Signature': signature}

        return methods.get(method)(path, data=params, headers=headers, base_url=base_url)

