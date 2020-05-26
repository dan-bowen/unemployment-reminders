import urllib
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
        """
        base_url = 'http://localhost'
        methods = {
            'GET': self.client.get,
            'POST': self.client.post
        }

        if valid:
            signature = self.twilio_client.compute_signature(method, f'{base_url}{path}', params)
        else:
            signature = self.twilio_client.compute_signature(method, f'{base_url}{path}/invalid', params)

        headers = {'X-Twilio-Signature': signature}

        return methods.get(method)(path, data=params, headers=headers, base_url=base_url)

