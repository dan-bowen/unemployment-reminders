from datetime import datetime
from wsgi import app
from bot import ReminderBot, ReminderBotException
from bot.repo import AlertsRepo
from bot.collect import CollectNextAlert

repo = AlertsRepo()
bot = ReminderBot(app)


def lambda_handler(event, context):
    pending_alerts = repo.get_pending_alerts()
    in_progress_alerts = apply_in_progress(pending_alerts)
    sms_alerts = send_sms(in_progress_alerts)
    return pending_alerts


def apply_in_progress(alerts):
    for alert in alerts:
        repo.set_in_progress(alert['phone_number'])
    return alerts


def send_sms(alerts):
    for alert in alerts:
        try:
            bot.say_reminder(alert['phone_number'])
            # only apply next alert if current alert is sent successfully
            apply_next_alert(alert)
        except ReminderBotException as e:
            print(e)
    return alerts


def apply_next_alert(alert):
    # pin "now" to the previous "next_alert_at" so we don't introduce drift from the original alert
    now = datetime.fromisoformat(alert['next_alert_at'])
    next_alert = CollectNextAlert(f"next {alert['alert_day']}",
                                  timezone=alert['timezone'],
                                  alert_time=alert['alert_time'])

    repo.set_next_alert(alert['phone_number'], next_alert.next_alert_at(now).isoformat())
