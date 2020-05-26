from flask import Blueprint, request
from lib.collect import CollectCertificationDate
from lib.twilio import validate_twilio_request, TwilioBot

blueprint = Blueprint('twilio', __name__)


@blueprint.route('/twilio/ping', methods=['POST'])
@validate_twilio_request
def ping():
    """Simple route for testing Twilio request validation"""
    return {'hello': 'world'}


@blueprint.route('/twilio/validate-certification-date', methods=['POST'])
@validate_twilio_request
def validate_certification_date():
    form_post = request.form
    is_valid = CollectCertificationDate(form_post['CurrentInput']).is_valid

    return {'valid': is_valid}


@blueprint.route('/twilio/collect', methods=['POST'])
def collect():
    bot = TwilioBot()
    bot.collect_certification_date(request.form)

    return bot.say_thanks()
