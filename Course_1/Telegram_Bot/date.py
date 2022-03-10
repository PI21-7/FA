import calendar
import datetime

def week_definition(count):
    current_date = datetime.date.today()
    week_day = current_date.weekday()
    month_dates = list(calendar.Calendar().itermonthdays3(current_date.year, current_date.month))
    day_index = month_dates.index((current_date.year, current_date.month, current_date.day))
    if day_index - week_day + 6 + count*7 <= len(month_dates) and (month_dates[day_index - week_day + 6 + count*7] != month_dates[-1] and month_dates[day_index - week_day + count*7] != month_dates[0]):
        
        week_dates = month_dates[day_index - week_day + count*7], month_dates[day_index - week_day + 6 + count*7]

        start_day = datetime.date(week_dates[0][0], week_dates[0][1], week_dates[0][2])
        end_day = datetime.date(week_dates[1][0], week_dates[1][1], week_dates[1][2])
        start_day = start_day.strftime("%d.%m.%Y")
        end_day = end_day.strftime("%d.%m.%Y")

        return f"{start_day} - ", end_day, True
        
    else:
    	if count > 0:
    		start_day = datetime.date(month_dates[-7][0], month_dates[-7][1], month_dates[-7][2])
    		end_day = datetime.date(month_dates[-1][0], month_dates[-1][1], month_dates[-1][2])
    		start_day = start_day.strftime("%d.%m.%Y")
    		end_day = end_day.strftime("%d.%m.%Y")
    		return "конец", f"месяца!\n{start_day} - {end_day}", False
    	else:
        	start_day = datetime.date(month_dates[0][0], month_dates[0][1], month_dates[0][2])
        	end_day = datetime.date(month_dates[6][0], month_dates[6][1], month_dates[6][2])
        	start_day = start_day.strftime("%d.%m.%Y")
        	end_day = end_day.strftime("%d.%m.%Y")
        	return "конец месяца!", f"\n{start_day} - {end_day}", False