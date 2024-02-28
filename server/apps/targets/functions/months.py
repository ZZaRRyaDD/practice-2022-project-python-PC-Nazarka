import calendar
from datetime import date, timedelta


def add_months(old_date: date, months: int) -> date:
    """Funtion for add to old data some count months."""
    month = old_date.month - 1 + months
    year = old_date.year + month // 12
    month = month % 12 + 1
    day = min(old_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def calculate_count_month(
    date_first: date,
    date_second: date = date.today(),
) -> int:
    """Function return count between today and `created_at` date."""
    delta = 0
    while True:
        mdays = calendar.monthrange(date_first.year, date_first.month)[1]
        date_first += timedelta(days=mdays)
        if date_second < date_first:
            break
        delta += 1
    return delta
