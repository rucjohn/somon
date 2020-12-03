# _*_ coding:utf-8 _*_

from __future__ import absolute_import, unicode_literals

import datetime
import numbers

from celery.schedules import crontab_parser


CRON_INVALID_TYPE = """\
Argument cron spec needs to be of any of the following types: \
int, str, or an iterable type. {type!r} was given.\
"""

CRON_PATTERN_INVALID = """\
Invalid crontab pattern.  Valid range is {min}-{max}. \
'{value}' was found.\
"""


def cron_field(s):
    return '*' if s is None else s


def transform_now():
    now = datetime.datetime.now()
    info = {
        "minute": now.minute,
        "hour": now.hour,
        "day_of_month": now.day,
        "month_of_year": now.month,
        "day_of_week": now.weekday()
    }
    return info


def transform_cron_timer(timer_str):
    guide = timer_str.split()
    guide = guide[:5]
    guide.extend(['*'] * (5 - len(guide)))
    return {
        "minute": cron_field(guide[0]),
        "hour": cron_field(guide[1]),
        "day_of_month": cron_field(guide[2]),
        "month_of_year": cron_field(guide[3]),
        "day_of_week": cron_field(guide[4])
    }


class ParseException(Exception):
    """Raised by :class:`CronParser` when the input can't be parsed."""


class Cron(object):

    def __init__(self, minute='*', hour='*',  day_of_month='*', month_of_year='*', day_of_week='*'):
        self.minute = self._expand_cron_spec(minute, 60)
        self.hour = self._expand_cron_spec(hour, 24)
        self.day_of_week = self._expand_cron_spec(day_of_week, 7)
        self.day_of_month = self._expand_cron_spec(day_of_month, 31, 1)
        self.month_of_year = self._expand_cron_spec(month_of_year, 12, 1)

    @staticmethod
    def _expand_cron_spec(spec, max_, min_=0):

        if isinstance(spec, numbers.Integral):
            result = {spec}
        elif isinstance(spec, str):
            result = crontab_parser(max_, min_).parse(spec)
        else:
            raise TypeError(CRON_INVALID_TYPE.format(type=type(spec)))

        # assure the result does not preceed the min or exceed the max
        for number in result:
            if number >= max_ + min_ or number < min_:
                raise ValueError(CRON_PATTERN_INVALID.format(
                    min=min_, max=max_ - 1 + min_, value=number))
        return result

    def is_valid(self):
        now = transform_now()
        if now['minute'] in self.minute \
                and now['hour'] in self.hour \
                and now['day_of_week'] in self.day_of_week \
                and now['day_of_month'] in self.day_of_month \
                and now['month_of_year'] in self.month_of_year:
            return True
        else:
            return False