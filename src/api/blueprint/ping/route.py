from lib.repo.alerts import AlertsRepo
from flask import Blueprint
import requests

blueprint = Blueprint('ping', __name__)


@blueprint.route('/healthcheck', methods=['GET'])
def ping_detail():
    try:
        r = requests.get('https://www.google.com', timeout=5)
        external_http_result = 'success'
    except requests.exceptions.ConnectionError as e:
        external_http_result = 'connection_error'
    except requests.exceptions.Timeout as e:
        external_http_result = 'timeout'

    try:
        r = AlertsRepo().count_items()
        db_access_result = 'success'
    except Exception as e:
        db_access_result = 'exception'

    ping_result = dict(external_http_result=external_http_result, db_access_result=db_access_result)

    return ping_result
