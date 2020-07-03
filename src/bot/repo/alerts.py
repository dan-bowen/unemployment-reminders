from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key
from config import config
from lib.dynamo.client import DynamoClient
from bot.schema.alert import AlertSchema


dynamo_client = DynamoClient(config.DYNAMODB_ENDPOINT)


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

    def delete_alert(self, phone_number):
        response = dynamo_client.alerts_table.delete_item(
            Key={
                'phone_number': phone_number
            }
        )

        return response

    def get_pending_alerts(self):
        now = datetime.now(timezone.utc)
        response = dynamo_client.alerts_table.query(
            IndexName="gsi_queue",
            KeyConditionExpression=Key('in_progress').eq(0) & Key('next_alert_at').lt(now.isoformat()),
        )
        return response['Items']

    def set_in_progress(self, phone_number):
        response = dynamo_client.alerts_table.update_item(
            Key={
                'phone_number': phone_number
            },
            UpdateExpression="SET in_progress = :in_progress",
            ExpressionAttributeValues={
                ':in_progress': 1
            }
        )
        return response

    def set_next_alert(self, phone_number, next_alert_at):
        response = dynamo_client.alerts_table.update_item(
            Key={
                'phone_number': phone_number
            },
            UpdateExpression="SET in_progress = :in_progress, next_alert_at = :next_alert_at",
            ExpressionAttributeValues={
                ':in_progress': 0,
                ':next_alert_at': next_alert_at
            }
        )
        return response
