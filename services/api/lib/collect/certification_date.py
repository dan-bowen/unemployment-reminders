import re
from .exceptions import CollectException


class CollectCertificationDate:
    pattern = r"^(?P<prefix>next\s)?(?P<day_of_week>monday|tuesday|wednesday|thursday|friday)$"

    def __init__(self, date):
        self.date = date
        self.matches = re.search(self.pattern, self.date, re.IGNORECASE)

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
