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
    bot = TwilioBot(base_url=current_app.config['BOT_BASE_URL'])
    return bot.ask_certification_date()


@blueprint.route('/bot/validate-certification-date', methods=['POST'])
@validate_twilio_request
def validate_certification_date():
    form_post = request.form
    bot = TwilioBot(base_url=current_app.config['BOT_BASE_URL'])
    return bot.validate_next_alert(form_post['CurrentInput'])


@blueprint.route('/bot/say-thanks', methods=['POST'])
@validate_twilio_request
def collect():
    bot = TwilioBot(base_url=current_app.config['BOT_BASE_URL'])
    bot.collect_certification_date(request.form)

    return bot.say_thanks()
