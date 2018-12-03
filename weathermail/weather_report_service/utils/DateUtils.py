import datetime


class DateUtils(object):
    """
        date util methods
    """
    @staticmethod
    def get_same_day_n_year_ago(current_date, year):
        """
            return the same date or {year} years ago.

            @type current_date: datetime.datetime

            @postcondition: isinstance(return, type(current_date))
        """
        assert isinstance(current_date, (datetime.datetime, datetime.date)), type(current_date)
        assert year < datetime.datetime.utcnow().year

        previous_date = current_date
        if current_date.month == 2 and current_date.day == 29 :
            previous_date = previous_date.replace(day=28)

        return previous_date.replace(year=(previous_date.year - year))