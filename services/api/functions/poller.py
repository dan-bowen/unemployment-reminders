from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
# TODO Not thrilled with this hack. Find a better way to let python know about our packages
# TODO Imports in general are a little messy. Clean up app-wide
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

from datetime import datetime
from api.wsgi import app
from api.repo import AlertsRepo
from lib.twilio import TwilioBot
from lib.collect import CollectNextAlert

repo = AlertsRepo()
bot = TwilioBot(app)


def lambda_handler(event, context):
    pending_alerts = repo.get_pending_alerts()
    in_progress_alerts = apply_in_progress(pending_alerts)
    sms_alerts = send_sms(in_progress_alerts)
    next_alerts = apply_next_alert(sms_alerts)
    return pending_alerts


def apply_in_progress(alerts):
    for alert in alerts:
        repo.set_in_progress(alert['phone_number'])
    return alerts


def send_sms(alerts):
    for alert in alerts:
        # this is the Auto-pilot simulator
        if alert['phone_number'] == 'user':
            print('skipping simulator user')
            continue
        bot.say_reminder(alert['phone_number'])
    return alerts


def apply_next_alert(alerts):
    for alert in alerts:
        # pin "now" to the previous "next_alert_at"
        now = datetime.fromisoformat(alert['next_alert_at'])
        next_alert = CollectNextAlert(f"next {alert['certification_day']}",
                                      timezone=alert['timezone'],
                                      alert_time=alert['alert_time'])

        repo.set_next_alert(alert['phone_number'], next_alert.next_alert_at(now).isoformat())
    return alerts
