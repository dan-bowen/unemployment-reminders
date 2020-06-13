import json
import base64
import boto3
from botocore.exceptions import ClientError

# Create a Boto3 session
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
session = boto3.session.Session()
client = session.client(service_name='secretsmanager')


def get_secret(secret_name):
    """
    Get a secret from AWS Secrets Manager.

    If you need more information about configurations or implementing the sample code, visit the AWS docs:
    https://aws.amazon.com/developers/getting-started/python/

    In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    We rethrow the exception by default.
    """

    try:
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        else:
            # rethrow on any error codes we haven't accounted for above
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in secret_value_response:
            secrets = secret_value_response['SecretString']
        else:
            secrets = base64.b64decode(secret_value_response['SecretBinary'])

    # `secrets` variable is a JSON string. ex:
    # '{"MYSQL_USERNAME":"","MYSQL_PASSWORD":""}'
    return json.loads(secrets)
