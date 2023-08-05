from datetime import datetime, timedelta
import calendar
import copy
from typing import Optional

from typing import TYPE_CHECKING, List, Literal

if TYPE_CHECKING:
    from cron import Cron
    from sub_modules.part import Part

weekdays = {'Sun': 0, 'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6}  # en_US weekdays


class Seeker:
    """Create an instance of Seeker. Seeker objects search for execution times of a cron schedule.
    Args:
        cron (object): Cron object
        start_time (datetime): The start time for the schedule iterator
    """
    def __init__(self, cron: 'Cron', start_time: Optional[datetime] = None) -> None:
        if not cron.parts:
            raise LookupError('No schedule found')

        if start_time and isinstance(start_time, datetime):
            self.tz_info = start_time.tzinfo
            self.date = start_time
        else:
            raise ValueError('Input schedule start time is not a valid datetime object')

        if self.date.second > 0:
            # Add a minute to the date to prevent returning dates in the past
            self.date = self.date + timedelta(minutes=+1)

        self.start_time = self.date
        self.cron = cron
        self.date = self.start_time
        self.pristine = True

    def reset(self) -> None:
        """Resets the iterator."""
        self.pristine = True
        self.date = self.start_time

    def next(self) -> datetime:
        """Returns the time the schedule would run next.

        :return: The time the schedule would run next.
        """
        if self.pristine:
            self.pristine = False
        else:
            one_minute = timedelta(minutes=+1)
            # Ensure next is never now
            self.date = self.date + one_minute

        return self.find_date(getattr(self.cron, 'parts'))

    def prev(self) -> datetime:
        """Returns the time the schedule would have last run at.

        :returns: The time the schedule would have last run at.
        """
        self.pristine = False
        # Ensure prev and next cannot be same time
        self.date = self.date + timedelta(minutes=-1)
        return self.find_date(getattr(self.cron, 'parts'), True)

    def find_date(self, cron_parts: List['Part'], reverse: bool = False) -> datetime:
        """Returns the time the schedule would run next.

        :param cron_parts: List of all cron 'Part'.
        :param reverse: Whether to find the previous value instead of next.
        :returns: A new datetime object. The date the schedule would have executed at.
        :raise Exception: Unable to find execution time for schedule.
        """
        operation: Literal['add', 'subtract'] = 'add'
        if reverse:
            operation = 'subtract'
        retry = 24
        while retry:
            retry -= 1
            self._shift_month(cron_parts[3], operation)
            month_changed = self._shift_day(cron_parts[2], cron_parts[4], operation)
            if not month_changed:
                day_changed = self._shift_hour(cron_parts[1], operation)
                if not day_changed:
                    hour_changed = self._shift_minute(cron_parts[0], operation)
                    if not hour_changed:
                        break
        else:
            raise Exception('Unable to find execution time for schedule')

        return copy.deepcopy(self.date.replace(second=0, microsecond=0))

    def _shift_month(self, cron_month_part: 'Part', operation: Literal['add', 'subtract']) -> None:
        """Increments/decrements the month value of a date, until a month that matches the schedule is found.

        :param cron_month_part: The month 'Part' object.
        :param operation: The function to call on date: 'add' or 'subtract'.
        """
        while self.date.month not in cron_month_part.to_list():
            self.date = self._calc_months(self.date, 1, operation)

    def _shift_day(self, cron_day_part: 'Part', cron_weekday_part: 'Part', operation: Literal['add', 'subtract']) -> bool:
        """Increments/decrements the day value of a date, until a day that matches the schedule is found.

        :param cron_day_part: The days 'Part' object.
        :param operation: The function to call on date: 'add' or 'subtract'.
        :return: Whether the month of the date was changed.
        """
        current_month = self.date.month
        while self.date.day not in cron_day_part.to_list() or \
                weekdays.get(self.date.strftime("%a")) not in cron_weekday_part.to_list():
            if operation == 'add':
                self.date = self.date + timedelta(days=+1)
                self.date = self.date.replace(hour=0, minute=0, second=0)
            else:
                self.date = self.date + timedelta(days=-1)
                self.date = self.date.replace(hour=23, minute=59, second=59)
            if current_month != self.date.month:
                return True
        return False

    def _shift_hour(self, cron_hour_part: 'Part', operation: Literal['add', 'subtract']) -> bool:
        """Increments/decrements the hour value of a date, until an hour that matches the schedule is found.

        :param cron_hour_part: The hours 'Part' object
        :param operation: The function to call on date: 'add' or 'subtract'.
        :return: Whether or not the day of the date was changed.
        """
        current_day = self.date.day
        while self.date.hour not in cron_hour_part.to_list():
            if operation == 'add':
                self.date = self.date + timedelta(hours=+1)
                self.date = self.date.replace(minute=00, second=0)
            else:
                self.date = self.date + timedelta(hours=-1)
                self.date = self.date.replace(minute=59, second=59)
            if current_day != self.date.day:
                return True
        return False

    def _shift_minute(self, cron_minute_part: 'Part', operation: Literal['add', 'subtract']) -> bool:
        """Increments/decrements the minute value of a date, until a minute that matches the schedule is found.

        :param cron_minute_part: The minutes 'Part' object.
        :param operation: The function to call on date: 'add' or 'subtract'.
        :return: Whether or not the hour of the date was changed.
        """
        current_hour = self.date.hour
        while self.date.minute not in cron_minute_part.to_list():
            if operation == 'add':
                self.date = self.date + timedelta(minutes=+1)
                self.date = self.date.replace(second=0)
            else:
                self.date = self.date + timedelta(minutes=-1)
                self.date = self.date.replace(second=59)
            if current_hour != self.date.hour:
                return True
        return False

    @staticmethod
    def _calc_months(date: 'datetime', months: int, operation: Literal['add', 'subtract']) -> datetime:
        """Static method to increment/decrement the month value of a datetime Object.

        :param date: Date Object it increments/decrements the month value to.
        :param months: Number of months to add at the provided input date Object
        :param operation: The function to call on date: 'add' or 'subtract'.
        :return: The input datetime object incremented or decremented.
        """
        if operation == 'add':
            month = date.month - 1 + months
        else:
            month = date.month - 1 - months
        year = date.year + month // 12
        month = month % 12 + 1
        if operation == 'add':
            return date.replace(year=year, month=month, day=1, hour=00, minute=00, second=00)
        else:
            # Get the last day of the month
            max_month_day = calendar.monthrange(year, month)[1]
            return date.replace(year=year, month=month, day=max_month_day, hour=23, minute=59, second=59)
