from marshmallow import Schema, fields


class AlertSchema(Schema):
    """
    The schema of an alert in DynamoDB
    """
    phone_number = fields.Str()
    next_alert_at = fields.Str()
    in_progress = fields.Integer()
    timezone = fields.Str()
    certfication_day = fields.Str()
    alert_time = fields.Str()
