from flask import Blueprint, request, current_app
from lib.twilio import validate_twilio_request, TwilioBot

blueprint = Blueprint('twilio', __name__)


@blueprint.route('/bot/ping', methods=['POST'])
@validate_twilio_request
def ping():
    """Simple route for testing Twilio request validation"""
    return {'hello': 'world'}


@blueprint.route('/bot/say-intro', methods=['POST'])
def say_intro():
    twilio_bot = TwilioBot(app=current_app)
    twilio_bot.say_intro(request.form['phone_number'])
    return {}


@blueprint.route('/bot/ask-next-alert', methods=['POST'])
@validate_twilio_request
def ask_next_alert():
    twilio_bot = TwilioBot(app=current_app)
    return twilio_bot.ask_next_alert()


@blueprint.route('/bot/validate-next-alert', methods=['POST'])
@validate_twilio_request
def validate_next_alert():
    twilio_bot = TwilioBot(app=current_app)
    return twilio_bot.validate_next_alert(request.form)


@blueprint.route('/bot/say-thanks', methods=['POST'])
@validate_twilio_request
def subscribe():
    twilio_bot = TwilioBot(app=current_app)
    twilio_bot.collect_next_alert(request.form)
    phone_number = request.form['UserIdentifier']
    twilio_bot.collect_phone_number(phone_number)
    twilio_bot.subscribe()
    return twilio_bot.say_thanks()


@blueprint.route('/bot/unsubscribe', methods=['POST'])
@validate_twilio_request
def unsubscribe():
    twilio_bot = TwilioBot(app=current_app)
    twilio_bot.unsubscribe(request.form)
    return twilio_bot.say_goodbye()


@blueprint.route('/bot/fallback', methods=['POST'])
@validate_twilio_request
def fallback():
    twilio_bot = TwilioBot(app=current_app)
    return twilio_bot.say_fallback()
