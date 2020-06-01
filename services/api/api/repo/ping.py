from lib.dynamo.client import DynamoClient


class PingRepo:
    def __init__(self, app):
        self.dynamo = DynamoClient(endpoint_url=app.config['DYNAMODB_ENDPOINT'])

    def ping_db(self):
        """
        ping the database
        """

        return self.dynamo.table_reminders.item_count
