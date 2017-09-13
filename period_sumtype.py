""" Python Algebraic Data Types (ADTs)

    `Period` example from `Stupid Python Ideas`
    Implemented in using SumTypes Python package
"""

# %%
from datetime import date
from sumtypes import sumtype, constructor, match

import attr


@sumtype
class PeriodSumtype(object):
    DurationPeriod = constructor('start_date', 'duration')
    DatePeriod = constructor('end_date', 'start_date')

# type durationPeriod = end_date * duration
# type datePeriod = end_date * start_date
# type Period = durationPeriod | datePeriod


# type printPeriod = Period -> String
@match(PeriodSumtype)
class print_period(object):
    def DurationPeriod(start_date, duration):
        return "start_date: {0}\n  duration: {1}".format(
            str(start_date), str(duration)),
    def DatePeriod(start_date, end_date):
        return "start_date: {0}\n  end_date: {1}".format(
            str(start_date), str(end_date))

start = date(2017, 7, 28)
end = date(2017, 8, 28)
duration = "1M"

print("DurationPeriod:\n{}".format(
    print_period(PeriodSumtype.DurationPeriod(start, duration))))
print("DatePeriod:\n{}".format(
    print_period(PeriodSumtype.DatePeriod(start, end))))

print("Finished...")


# %%
@sumtype
class PeriodAttrtype(object):
    DurationPeriod = constructor(
        start_date=attr.ib(validator=attr.validators.instance_of(date)),
        duration=attr.ib(validator=attr.validators.instance_of(str)))
    DatePeriod = constructor(
        start_date=attr.ib(validator=attr.validators.instance_of(date)),
        end_date=attr.ib(validator=attr.validators.instance_of(date)))

@sumtype
class Implementation(object):
    Sumtype = constructor(
        sum_type=attr.ib(validator=attr.validators.instance_of(PeriodSumtype)))
    Attrtype = constructor(
        attr_type=attr.ib(validator=attr.validators.instance_of(PeriodAttrtype)))


# type matchPeriod = Period -> Period
@match(Implementation)
class match_impl(object):
    def Sumtype(sum_type): return sum_type
    def Attrtype(attr_type): return attr_type

sum_dur = PeriodSumtype.DurationPeriod(start, duration)
sum_dat = PeriodSumtype.DatePeriod(start, end)

att_dur = PeriodAttrtype.DurationPeriod(start, duration)
att_dat = PeriodAttrtype.DatePeriod(start, end)

sum_type = Implementation.Sumtype(sum_dat)
attr_type = Implementation.Attrtype(att_dat)

print("Sumtype: {}".format(match_impl(sum_type)))
print("Attrtype: {}".format(match_impl(attr_type)))

print("Finished...")
