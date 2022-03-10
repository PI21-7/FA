import datetime

def week_definition(count):
    current_date  = datetime.date.today()
    week_day = datetime.timedelta(days=current_date.weekday())
    end_week = datetime.timedelta(days=6)
    week = datetime.timedelta(weeks=1)
    start_date = current_date - week_day + count * week
    end_date = current_date - week_day + end_week + count * week
    return start_date.strftime("%d.%m.%y"), end_date.strftime("%d.%m.%y")