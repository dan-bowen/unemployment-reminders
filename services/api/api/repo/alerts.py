from api.extension import dynamo_client
from api.schema.alert import AlertSchema


class AlertsRepo:
    def __init__(self):
        pass

    def count_items(self):
        """
        Get number of items in the DB

        Per the AWS documentation:
        DynamoDB updates this value approximately every six hours. Recent changes might not be reflected in this value.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.describe_table
        """

        return dynamo_client.alerts_table.item_count

    def create_alert(self, alert_model):
        response = dynamo_client.alerts_table.put_item(
            Item=AlertSchema().dump(alert_model)
        )
        return response
