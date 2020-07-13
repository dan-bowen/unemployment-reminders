"""
Lambda function that sends alerts

Invoked via CloudWatch events on a schedule.
"""
from datetime import datetime
from bot import ReminderBot, ReminderBotException
from bot.collect import CollectNextAlert
from bot.repo import alerts as alerts_repo

bot = ReminderBot()


def lambda_handler(event, context):
    pending_alerts = alerts_repo.get_pending_alerts()
    in_progress_alerts = apply_in_progress(pending_alerts)
    sms_alerts = send_sms(in_progress_alerts)
    return pending_alerts


def apply_in_progress(alerts):
    """
    Apply the in_progress flag to alerts

    Prevents other processes from picking them up while being processed
    """
    for alert in alerts:
        alerts_repo.set_in_progress(alert['phone_number'])
    return alerts


def send_sms(alerts):
    for alert in alerts:
        try:
            bot.say_reminder(alert['phone_number'])
            # only apply next alert if current alert is sent successfully
            apply_next_alert(alert)
        except ReminderBotException as e:
            # TODO decide what to do here. Retry logic will depend on specific exception raised
            print(e)

    return alerts


def apply_next_alert(alert):
    # pin "now" to the previous "next_alert_at" so we don't introduce drift from the original alert
    now = datetime.fromisoformat(alert['next_alert_at'])
    next_alert = CollectNextAlert(f"next {alert['alert_day']}",
                                  timezone=alert['timezone'],
                                  alert_time=alert['alert_time'])

    alerts_repo.set_next_alert(alert['phone_number'], next_alert.next_alert_at(now).isoformat())
