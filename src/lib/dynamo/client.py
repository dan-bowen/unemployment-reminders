import boto3


class DynamoClient:
    def __init__(self, endpoint_url=None):
        self.dynamo = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        self.alerts_table = self.dynamo.Table('unemployment-reminders')
