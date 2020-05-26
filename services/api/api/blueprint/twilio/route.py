import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from lib.collect import CollectCertificationDate
from lib.twilio import validate_twilio_request

blueprint = Blueprint('twilio', __name__)


@blueprint.route('/twilio/ping', methods=['POST'])
@validate_twilio_request
def ping():
    """Simple route for testing Twilio request validation"""
    return {'hello': 'world'}
