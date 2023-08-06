# !/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime as dt
import math


START_IN_REAL_TIME = '2000-01-01_00:00:00'
DATE_FORMAT = '%Y-%m-%d_%H:%M:%S'
FAME_FIRST_DATETIME = dt.datetime.strptime(START_IN_REAL_TIME, DATE_FORMAT)

# Constants
STEPS_PER_SECOND = 1
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_YEAR = 365
STEPS_PER_MINUTE = STEPS_PER_SECOND * SECONDS_PER_MINUTE
STEPS_PER_HOUR = STEPS_PER_MINUTE * MINUTES_PER_HOUR
STEPS_PER_DAY = STEPS_PER_HOUR * HOURS_PER_DAY
STEPS_PER_YEAR = STEPS_PER_DAY * DAYS_PER_YEAR


class FameTime:
    """Handles conversion of TimeSteps into TimeStamps and vice versa"""

    @staticmethod
    def convert_time_string_to_fame_time_step(datetime_string):
        """Converts real Datetime string to FAME time step"""
        datetime = dt.datetime.strptime(datetime_string, DATE_FORMAT)
        years_since_start_time = datetime.year - FAME_FIRST_DATETIME.year
        beginning_of_year = dt.datetime(year=datetime.year, month=1, day=1, hour=0, minute=0, second=0)
        seconds_since_beginning_of_year = (datetime - beginning_of_year).total_seconds()
        return years_since_start_time * STEPS_PER_YEAR + seconds_since_beginning_of_year

    @staticmethod
    def convert_fame_time_step_to_datetime_string(fame_time_steps):
        """Converts fame time step to Datetime string"""
        years_since_start_time = math.floor(fame_time_steps / STEPS_PER_YEAR)
        current_year = years_since_start_time + 2000
        beginning_of_year = dt.datetime(year=current_year, month=1, day=1, hour=0, minute=0, second=0)
        seconds_in_current_year = fame_time_steps - years_since_start_time * STEPS_PER_YEAR
        datetime = beginning_of_year + dt.timedelta(seconds=seconds_in_current_year)
        return datetime.strftime(DATE_FORMAT)
