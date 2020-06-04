from flask import Blueprint, request, current_app
from api.extension import twilio_bot
from lib.twilio import validate_twilio_request

blueprint = Blueprint('twilio', __name__)


@blueprint.route('/bot/ping', methods=['POST'])
@validate_twilio_request
def ping():
    """Simple route for testing Twilio request validation"""
    return {'hello': 'world'}


@blueprint.route('/bot/ask-certification-date', methods=['POST'])
@validate_twilio_request
def ask_certification_date():
    return twilio_bot.ask_certification_date()


@blueprint.route('/bot/validate-certification-date', methods=['POST'])
@validate_twilio_request
def validate_certification_date():
    return twilio_bot.validate_next_alert(request.form)


@blueprint.route('/bot/say-thanks', methods=['POST'])
@validate_twilio_request
def collect():
    twilio_bot.collect_certification_date(request.form)
    alert_model = dict(phone_number=7735551234, next_alert_at='', in_progress=0, timezone='America/Chicago',
                       certification_day='wednesday', alert_time='09:30:00')

    return twilio_bot.say_thanks()
