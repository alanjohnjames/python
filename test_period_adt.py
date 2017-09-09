""" Python Algebraic Data Types (ADTs)

    `Period` example from `Stupid Python Ideas`

    The code below is based on the last comment post:
    http://stupidpythonideas.blogspot.co.uk/2014/08/adts-for-python.html 

    Kris Nuttycombe (17 August, 2016 15:36)
    I know it's ugly as hell, but I get by by encoding my sum type values in terms of their catamorphism.
    Then, at least, "pattern matching" on them is just a function call.
    Here's an example below...
"""

# %%
from datetime import date

# type durationPeriod = end_date * duration
# type datePeriod = end_date * start_date
# type Period = durationPeriod | datePeriod

def duration_period(start_date, duration):
    return lambda if_duration, if_date: if_duration(start_date, duration)

def date_period(end_date, start_date):
    return lambda if_duration, if_date: if_date(end_date, start_date)

# In what way are `duration_period` and `date_period` a data type (class) ?
# I suppose `duration_period` and `date_period` could be methods (type ctors) in class Period


# type printPeriod = Period -> String
def print_period(period):  # period -> match_period
    return period(
        if_duration = lambda start_date, duration:
            "  start_date: {0}\n  duration: {1}".format(str(start_date), str(duration)), 
        if_date = lambda start_date, end_date:
            "  start_date: {0}\n  end_date: {1}".format(str(start_date), str(end_date)))

# type Tenor = Days | Months | Years

# type calcPeriod = Period -> Tenor
def calc_period(period):
    return period(
        if_duration = lambda end_date, duration: duration,
        if_date = lambda start_date, end_date: end_date - start_date)


start = date(2017, 7, 28)
end = date(2017, 8, 28)
duration = "1M"

print("print_period...")
print("date_period:\n{}".format(print_period(date_period(start, end))))
print("duration_period:\n{}".format(print_period(duration_period(start, duration))))

print("calc_period...")
print("date_period:\n  {}".format(calc_period(date_period(start, end))))
print("duration_period:\n {}".format(calc_period(duration_period(start, duration))))
