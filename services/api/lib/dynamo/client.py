import boto3


class DynamoClient:
    def __init__(self, endpoint_url=None):
        if endpoint_url:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        else:
            self.dynamodb = boto3.resource('dynamodb')

        self.table_reminders = self.dynamodb.Table('unemployment-reminders')
