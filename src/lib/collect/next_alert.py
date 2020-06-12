import re
import pytz
from datetime import datetime, time
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR
from .exceptions import CollectException


class CollectNextAlert:
    """
    Collects certification date from user and calculates next alert date.
    """

    pattern = r"^(?P<prefix>next\s)?(?P<day_of_week>monday|tuesday|wednesday|thursday|friday)$"
    weekdays = {
        'monday':    MO,
        'tuesday':   TU,
        'wednesday': WE,
        'thursday':  TH,
        'friday':    FR
    }

    def __init__(self, date, timezone='America/Chicago', alert_time='09:30:00'):
        self.date = date
        self.matches = re.search(self.pattern, self.date.strip(), re.IGNORECASE)
        self.timezone = timezone
        self.alert_time = time.fromisoformat(alert_time)

    def _raise_invalid(self):
        if not self.is_valid:
            raise CollectException('Certification date is invalid')

    @property
    def is_valid(self):
        return bool(self.matches)

    @property
    def sequence(self):
        self._raise_invalid()
        return 1 if self.matches.group('prefix') else 0

    @property
    def day_of_week(self):
        self._raise_invalid()
        return self.matches.group('day_of_week').lower()

    def next_alert_at(self, now):
        """
        Get date of next alert

        SEE https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python

        :param now: Timezone aware datetime
        :type now: datetime.datetime
        :return: Timezone aware (UTC) datetime object
        """
        local_now = now.astimezone(pytz.timezone(self.timezone))
        day_of_week = self.weekdays.get(self.day_of_week)

        if self.sequence == 1:
            """
            2 {day_of_week}s from today, but not today
            
            Example
            -------
            input: next monday
            next_alert: 2 mondays after today
            """
            next_alert = local_now + relativedelta(days=+1, weekday=day_of_week(+2))
        else:
            """
            1 {day_of_week} from today, but not today

            Example
            -------
            input: monday
            next_alert: 1 monday after today
            """
            next_alert = local_now + relativedelta(days=+1, weekday=day_of_week(+1))

        next_alert = next_alert.replace(hour=self.alert_time.hour, minute=self.alert_time.minute,
                                        second=self.alert_time.second, microsecond=0)
        return next_alert.astimezone(pytz.timezone('UTC'))
