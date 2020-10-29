# Function to calculate days in between start and finish
import datetime
def day_num(start_date, end_date):
    delta = datetime.timedelta(days=1)
    count = 0
    while start_date <= end_date:
        count += 1
        start_date += delta
    return(count)
