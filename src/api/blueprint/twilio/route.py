from flask import Blueprint, request
from lib.twilio import validate_twilio_request
from api.extension import bot

blueprint = Blueprint('twilio', __name__)


@blueprint.route('/bot/ping', methods=['POST'])
@validate_twilio_request
def ping():
    """Simple route for testing Twilio request validation"""
    return {'hello': 'world'}


@blueprint.route('/bot/say-intro', methods=['POST'])
def say_intro():
    bot.say_intro(request.form['phone_number'])
    return {}


@blueprint.route('/bot/ask-next-alert', methods=['POST'])
@validate_twilio_request
def ask_next_alert():
    return bot.ask_next_alert()


@blueprint.route('/bot/validate-next-alert', methods=['POST'])
@validate_twilio_request
def validate_next_alert():
    return bot.validate_next_alert(request.form)


@blueprint.route('/bot/say-thanks', methods=['POST'])
@validate_twilio_request
def subscribe():
    bot.collect_next_alert(request.form)
    phone_number = request.form['UserIdentifier']
    bot.collect_phone_number(phone_number)
    bot.subscribe()
    return bot.say_thanks()


@blueprint.route('/bot/unsubscribe', methods=['POST'])
@validate_twilio_request
def unsubscribe():
    bot.unsubscribe(request.form)
    return bot.say_goodbye()


@blueprint.route('/bot/found-a-job', methods=['POST'])
@validate_twilio_request
def found_a_job():
    bot.unsubscribe(request.form)
    return bot.say_congrats()


@blueprint.route('/bot/fallback', methods=['POST'])
@validate_twilio_request
def fallback():
    return bot.say_fallback()
