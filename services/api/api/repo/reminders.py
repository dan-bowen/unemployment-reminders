from lib.dynamo.client import DynamoClient


class RemindersRepo:
    def __init__(self, app):
        self.dynamo = DynamoClient(endpoint_url=app.config['DYNAMODB_ENDPOINT'])

    def count_items(self):
        """
        Get number of items in the DB

        Per the AWS documentation:
        DynamoDB updates this value approximately every six hours. Recent changes might not be reflected in this value.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_table
        """

        return self.dynamo.table_reminders.item_count
