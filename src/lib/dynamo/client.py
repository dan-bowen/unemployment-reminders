import boto3


class DynamoClient:
    def __init__(self, app=None):
        self.app = app
        self.dynamo = None
        self.alerts_table = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        endpoint_url = app.config['DYNAMODB_ENDPOINT']
        if endpoint_url:
            self.dynamo = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        else:
            self.dynamo = boto3.resource('dynamodb')

        self.alerts_table = self.dynamo.Table('unemployment-reminders')
