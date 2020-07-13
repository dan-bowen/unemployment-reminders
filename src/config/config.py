"""
Set up config according to 12-Factor best practices.

@see https://12factor.net/config
"""
import os
import marshmallow
from lib.secrets.secrets_manager import get_secret


class Secrets:
    def __init__(self, secrets):
        try:
            secrets_from_schema = self.ExpectedSecretsSchema().load(secrets)
        except marshmallow.ValidationError as e:
            raise e

        self.SECRET_KEY = secrets_from_schema['SECRET_KEY']
        self.TWILIO_ACCOUNT_SID = secrets_from_schema['TWILIO_ACCOUNT_SID']
        self.TWILIO_AUTH_TOKEN = secrets_from_schema['TWILIO_AUTH_TOKEN']

    class ExpectedSecretsSchema(marshmallow.Schema):
        SECRET_KEY = marshmallow.fields.String(required=True)
        TWILIO_ACCOUNT_SID = marshmallow.fields.String(required=True)
        TWILIO_AUTH_TOKEN = marshmallow.fields.String(required=True)


def secrets_from_env():
    return dict(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        TWILIO_ACCOUNT_SID=os.getenv('TWILIO_ACCOUNT_SID'),
        TWILIO_AUTH_TOKEN=os.getenv('TWILIO_AUTH_TOKEN')
    )


class BaseConfig:
    """
    BaseConfig

    All other configs inherit from this.
    """

    def __init__(self):
        #######
        # APP #
        #######
        self.SECRETS = Secrets(dict(SECRET_KEY='', TWILIO_ACCOUNT_SID='', TWILIO_AUTH_TOKEN=''))
        self.BOT_BASE_URL = os.getenv('BOT_BASE_URL')
        self.BOT_SMS_NUMBER = os.getenv('BOT_SMS_NUMBER')
        self.DYNAMODB_ENDPOINT = None
        self.API_GATEWAY_BASE_PATH = None

        #########
        # FLASK #
        #########
        self.DEBUG = False
        self.TESTING = False
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


class DevConfig(BaseConfig):
    """Dev configuration."""

    def __init__(self):
        super().__init__()
        #######
        # APP #
        #######
        self.SECRETS = Secrets(get_secret(os.getenv('SECRETS_MANAGER_SECRET_ARN')))
        self.BOT_BASE_URL = os.getenv('BOT_BASE_URL')
        self.BOT_SMS_NUMBER = os.getenv('BOT_SMS_NUMBER')
        self.DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT')
        self.API_GATEWAY_BASE_PATH = os.getenv('API_GATEWAY_BASE_PATH')

        #########
        # FLASK #
        #########
        self.DEBUG = True
        self.TESTING = False
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


class StageConfig(BaseConfig):
    """Stage configuration."""

    def __init__(self):
        super().__init__()
        #######
        # APP #
        #######
        self.SECRETS = Secrets(get_secret(os.getenv('SECRETS_MANAGER_SECRET_ARN')))
        self.BOT_BASE_URL = os.getenv('BOT_BASE_URL')
        self.BOT_SMS_NUMBER = os.getenv('BOT_SMS_NUMBER')
        self.DYNAMODB_ENDPOINT = None
        self.API_GATEWAY_BASE_PATH = os.getenv('API_GATEWAY_BASE_PATH')

        #########
        # FLASK #
        #########
        self.DEBUG = False
        self.TESTING = False
        self.SECRET_KEY = self.SECRETS.SECRET_KEY


class TestConfig(BaseConfig):
    """Test configuration."""

    def __init__(self):
        super().__init__()
        #######
        # APP #
        #######
        self.SECRETS = Secrets(secrets_from_env())
        self.BOT_BASE_URL = os.getenv('BOT_BASE_URL')
        self.BOT_SMS_NUMBER = os.getenv('BOT_SMS_NUMBER')
        self.DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT')
        self.API_GATEWAY_BASE_PATH = os.getenv('API_GATEWAY_BASE_PATH')

        #########
        # FLASK #
        #########
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
