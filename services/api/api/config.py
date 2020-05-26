"""
Set up config according to 12-Factor best practices.

@see https://12factor.net/config
"""

import os
import json
import base64
import marshmallow
import boto3
from botocore.exceptions import ClientError

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Secrets:
    def __init__(self, secrets):
        try:
            secrets_from_schema = self.ExpectedSecretsSchema().load(secrets)
        except marshmallow.ValidationError as e:
            raise e

        self.SECRET_KEY = secrets_from_schema['SECRET_KEY']
        self.TWILIO_AUTH_TOKEN = secrets_from_schema['TWILIO_AUTH_TOKEN']

    class ExpectedSecretsSchema(marshmallow.Schema):
        SECRET_KEY = marshmallow.fields.String(required=True)
        TWILIO_AUTH_TOKEN = marshmallow.fields.String(required=True)


class SecretsFromEnv:
    """
    Get secrets from ENV vars. This is not the preferred way but will enable local development
    and testing without making API calls to AWS Secret Manager.
    """

    def __init__(self):
        self._data = dict(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')
        )

    def get_secrets(self):
        return self._data


class SecretsFromSecretsManager:
    def __init__(self):
        # Create a Boto3 session
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
        self._session = boto3.session.Session()

        # Create a Secrets Manager client
        self._client = self._session.client(
            service_name='secretsmanager'
        )

        self._secret_name = os.getenv('SECRETS_MANAGER_SECRET_ARN')

    def get_secrets(self):
        """
        Get secrets from AWS Secrets Manager.

        If you need more information about configurations or implementing the sample code, visit the AWS docs:
        https://aws.amazon.com/developers/getting-started/python/
        """

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.

        try:
            secret_value_response = self._client.get_secret_value(
                SecretId=self._secret_name
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


class BaseConfig:
    """
    BaseConfig

    All other configs inherit from this.
    """

    def __init__(self):
        #####################
        # APP configuration #
        #####################
        self.SECRETS = Secrets(dict(SECRET_KEY='', TWILIO_AUTH_TOKEN=''))
        self.BASE_DIR = basedir

        #######################
        # FLASK configuration #
        #######################
        self.DEBUG = False
        self.TESTING = False
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


class DevConfig(BaseConfig):
    """Dev configuration."""

    def __init__(self):
        super().__init__()

        #####################
        # APP configuration #
        #####################
        self.SECRETS = Secrets(SecretsFromSecretsManager().get_secrets())
        self.BASE_DIR = basedir

        #######################
        # FLASK configuration #
        #######################
        self.DEBUG = True
        self.TESTING = False
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


class StageConfig(BaseConfig):
    """Stage configuration."""

    def __init__(self):
        super().__init__()

        #####################
        # APP configuration #
        #####################
        self.SECRETS = Secrets(SecretsFromSecretsManager().get_secrets())
        self.BASE_DIR = basedir

        #######################
        # FLASK configuration #
        #######################
        self.DEBUG = False
        self.TESTING = False
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


class TestConfig(BaseConfig):
    """Test configuration."""

    def __init__(self):
        super().__init__()

        #####################
        # APP configuration #
        #####################
        self.SECRETS = Secrets(SecretsFromEnv().get_secrets())
        self.BASE_DIR = basedir

        #######################
        # FLASK configuration #
        #######################
        self.DEBUG = False
        self.TESTING = True
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


def get_config():
    """
    Get fully loaded configuration object for the environment.

    :return:
    """
    env = os.getenv('FLASK_ENV', 'default')

    # Map environments to config classes
    config_map = {
        "default": DevConfig,
        "dev":     DevConfig,
        "test":    TestConfig,
        "stage":   StageConfig
    }

    config_class = config_map.get(env)

    return config_class()
