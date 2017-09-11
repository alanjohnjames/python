""" Python Algebraic Data Types (ADTs)

    `Period` example from `Stupid Python Ideas`
    Implemented in using SumTypes and Attr Python package
"""

# %%
from datetime import date
from sumtypes import sumtype, constructor, match

# from attr import attrs, attrib

import attr


# %%

@attr.s
class SomeClass(object):
    a_number = attr.ib(default=42)
    list_of_numbers = attr.ib(default=attr.Factory(list))

SomeClass(1, [])
sc = SomeClass(1, [1, 2, 3])
print(sc)


# %%
@attr.s
class PeriodTest(object):
    start_date = attr.ib(validator=attr.validators.instance_of(date))
    duration = attr.ib(validator=attr.validators.instance_of(str))


dur = PeriodTest(date(2017, 9, 11), "1Y")
print("Dur: {}".format(dur))

print("What happened...?")

# %%

@attr.s
class DurationPeriod(object):
    start_date = attr.ib(validator=attr.validators.instance_of(date))
    duration = attr.ib(validator=attr.validators.instance_of(str))


@attr.s
class DatePeriod(object):
    start_date = attr.ib(validator=attr.validators.instance_of(date))
    end_date = attr.ib(validator=attr.validators.instance_of(date))


@sumtype
class PeriodAttr(object):
    Duration = constructor(
        dur_period=attr.ib(validator=attr.validators.instance_of(DurationPeriod)))
    Date = constructor(
        dat_period=attr.ib(validator=attr.validators.instance_of(DatePeriod)))

start = date(2017, 7, 28)
end = date(2017, 8, 28)
duration = "1M"

dur = DurationPeriod(start, duration)
dt = DatePeriod(start, end)
print("Dur: {}".format(dur))


# %%
# type printPeriod = Period -> String
@match(PeriodAttr)
class print_period(object):
    def Duration(p):
        return "start_date: {0}\n  duration: {1}".format(
            str(p.start_date), str(p.duration))
    def Date(p):
        return "start_date: {0}\n  end_date: {1}".format(
            str(p.start_date), str(p.end_date))


durattr = PeriodAttr.Duration(dur)

print(print_period(durattr))

print("DurationPeriod:\n{}".format(
    print_period(PeriodAttr.Duration(dur))))
print("DatePeriod:\n{}".format(
    print_period(PeriodAttr.Date(dt))))


print("Finished...")
