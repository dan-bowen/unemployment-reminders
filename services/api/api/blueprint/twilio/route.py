from flask import Blueprint, request, current_app
from lib.twilio import validate_twilio_request, TwilioBot

blueprint = Blueprint('twilio', __name__)


@blueprint.route('/bot/ping', methods=['POST'])
@validate_twilio_request
def ping():
    """Simple route for testing Twilio request validation"""
    return {'hello': 'world'}


@blueprint.route('/bot/ask-certification-date', methods=['POST'])
@validate_twilio_request
def ask_certification_date():
    twilio_bot = TwilioBot(current_app)
    return twilio_bot.ask_next_alert()


@blueprint.route('/bot/validate-certification-date', methods=['POST'])
@validate_twilio_request
def validate_certification_date():
    twilio_bot = TwilioBot(current_app)
    return twilio_bot.validate_next_alert(request.form)


@blueprint.route('/bot/say-thanks', methods=['POST'])
@validate_twilio_request
def collect():
    twilio_bot = TwilioBot(current_app)
    twilio_bot.collect_next_alert(request.form)

    return twilio_bot.say_thanks()
